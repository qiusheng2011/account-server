import hashlib
import logging
import secrets
import datetime
from typing import Optional

from sqlalchemy.ext import asyncio as sqlalchemy_asyncio
from jose import jwt, exceptions as jose_exceptions
from redis import asyncio as asyncio_redis

from src.app.modules.account import model
from src.app.modules.account import dbmodel
from src.app.modules.account import exception_errors
from src.app.tool import tool
from src.app.modules.account import events

logger = logging.getLogger(__name__)


class AccountManager():
    """账户管理器
    """

    def __init__(self, async_dbsessionmaker: sqlalchemy_asyncio.async_sessionmaker, async_event_db_pool: Optional[asyncio_redis.ConnectionPool] = None):
        self.async_dbsessionmaker = async_dbsessionmaker
        self.async_event_db_pool = async_event_db_pool
        self.logger = logging.getLogger(__name__)
        self.db_account_operater = dbmodel.DBAccountOperater()

    async def register(self, account: model.Account, activate_token: str = ""):
        """注册一个账户
        """
        try:
            if not activate_token:
                activate_token = secrets.token_urlsafe(48)
            dbaccount = dbmodel.DBAccount(
                **account.model_dump(exclude_unset=True))
            async with self.async_dbsessionmaker.begin() as async_session:
                check_result, gdbaccount = await self.db_account_operater.check_accout_by_email_and_account_name(
                    async_session, dbaccount.email, dbaccount.account_name)
                if check_result and gdbaccount:
                    if gdbaccount.activation == 0:
                        raise exception_errors.AccountUnactivateError
                    else:
                        raise exception_errors.AccountExistError()
                async_session.add(dbaccount)
                await async_session.flush()
                account.aid = dbaccount.aid

                account_activation = model.AccountActivation(
                    aid=dbaccount.aid,
                    activate_token=activate_token,
                    expire_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
                    used=False
                )
                db_account_activation = dbmodel.DBAccountActivation(**account_activation.model_dump(exclude_unset=True))

                save_aa_ok = await self.db_account_operater.save_account_activation(async_session, db_account_activation)

                register_event = events.RegisterSuccessEvent(data={
                    "account_email": account.email,
                    "account_aid": account.aid,
                    "activate_token": account_activation.activate_token
                })
                async with asyncio_redis.Redis.from_pool(self.async_event_db_pool) as async_redis:
                    await async_redis.lpush("account_server", register_event.model_dump_json())
            return True
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def activate_account(self, activate_token):
        # 获取激活实体
        try:
            async with self.async_dbsessionmaker.begin() as async_session:
                db_account_activation = await self.db_account_operater.get_account_activation(async_session, activate_token)
                if not db_account_activation:
                    raise exception_errors.AccountActivationNotFoundError
                if not db_account_activation.used:
                    is_ok = await self.db_account_operater.accont_activate(async_session, db_account_activation)
                    return is_ok
                else:
                    raise exception_errors.AccountActivationHasUsedError

        except Exception as ex:
            logger.error(str(ex))
            raise ex

    def verify_account(self, account: model.Account, password: str):
        """ 验证账户
        """
        if account.hash_password == tool.get_hash_password(password):
            return True
        else:
            return False

    async def get_accounts_by_email(self, email):
        """获取账户
        """
        try:
            async with self.async_dbsessionmaker.begin() as async_session:
                is_exist, account = await self.db_account_operater.get_account_by_email(session=async_session, email=email)
                return (True, model.Account.model_validate(account)) if is_exist else (False, None)
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def authencicate_account(self, email: str, password: str):
        """校验账户
        """
        is_exist, account = await self.get_accounts_by_email(email)
        if not is_exist:
            return False, None
        elif is_exist and account:
            if not self.verify_account(account, password):
                return False, None
            return True, account

    async def authencicate_account_by_refresh_token(self, refresh_token: str):

        try:
            async with self.async_dbsessionmaker.begin() as async_session:
                is_exist, account = await self.db_account_operater.get_account_by_refresh_token(
                    async_session, refresh_token)
                return is_exist, model.Account.model_validate(account) if is_exist else None
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def delete_account(self, account: model.Account):
        """物理删除一个账户的所有信息。
        """
        try:
            async with self.async_dbsessionmaker.begin() as asyc_session:
                is_exist, db_account = await self.db_account_operater.get_account_by_aid(asyc_session, account.aid)
                if is_exist and db_account:
                    await self.db_account_operater.delete_dbaccount(asyc_session, db_account)
                    return True
                else:
                    raise ValueError(f"不存在的账户({account.aid})")
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def make_account_access_token(self, account: model.Account, token_expire_minutes: int = 10, token_secret_key: str = "", token_algorithm="", refresh_token_expire_extra_minutes: int = 1440):

        now = datetime.datetime.now(datetime.timezone.utc)
        now_dt = now + datetime.timedelta(minutes=token_expire_minutes)
        # TODO 加盐优化
        info = f"asdkfjkldsf#{account.account_name}#werdsfsdf#{str(now_dt)}"
        sub = hashlib.sha256(info.encode("utf8")).hexdigest()

        refresh_dt = now_dt + \
            datetime.timedelta(minutes=refresh_token_expire_extra_minutes)
        refresh_info = f"asdkfjkldsf#{
            account.email}#werdsfsdf#{str(refresh_dt)}"
        refresh_sub = hashlib.sha256(refresh_info.encode("utf8")).hexdigest()
        data = {
            "sub": sub,
            "exp": now_dt
        }
        encode_jwt = jwt.encode(
            data, str(token_secret_key), algorithm=token_algorithm)
        try:
            async with self.async_dbsessionmaker.begin() as async_session:
                await self.db_account_operater.save_account_token(
                    async_session, dbmodel.DBAccountCertificateToken(
                        aid=account.aid, token=sub, refresh_token=refresh_sub
                    )
                )
        except Exception as ex:
            logger.error(str(ex))
            raise ex

        return encode_jwt, refresh_sub, int(now.timestamp())

    async def get_account_by_token(self, token, token_secret_key: str = "", token_algorithm="") -> model.Account | None:
        try:
            payload = jwt.decode(token, str(
                token_secret_key), algorithms=token_algorithm)

            sub_token = payload.get("sub", "")
            expire_date = payload.get("exp", 0)
            utc_now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            if utc_now >= expire_date:
                return None
            async with self.async_dbsessionmaker.begin() as async_session:
                dbaccount = await self.db_account_operater.get_account_by_token(async_session, sub_token)
                return model.Account.model_validate(dbaccount) if dbaccount else None
        except jose_exceptions.ExpiredSignatureError:
            return None

        except Exception as ex:
            logger.error(str(ex))
            raise ex
