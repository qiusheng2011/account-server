from typing import Optional
import hashlib
from datetime import datetime, timedelta, timezone
from pydantic import (
    BaseModel
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as AsyncSessionFactory,
    AsyncSession
)
from jose import JWTError, jwt

from .model import Account
from .dbmodel import DBAccount, DBAccountOperater
from .exception import AccountExistError
from ...tool import get_hash_password


class AccountManager():
    """账户管理器
    """

    def __init__(self, async_dbsessionmaker: AsyncSessionFactory):
        self.async_dbsessionmaker = async_dbsessionmaker

    async def register(self, account: Account):
        """注册一个账户
        """
        dbaccount = DBAccount(**account.model_dump(exclude_unset=True))
        async with self.async_dbsessionmaker.begin() as async_session:
            check_result = await DBAccountOperater.check_accout_by_email_and_account_name(async_session, dbaccount.email, dbaccount.account_name)
            if check_result:
                raise AccountExistError()
            async_session.add(dbaccount)
            await async_session.flush()
            account.aid = dbaccount.aid
        return True

    def verify_account(self, account: Account, password: str):
        """ 验证账户
        """
        if account.hash_password == get_hash_password(password):
            return True
        else:
            return False

    async def get_accounts_by_email(self, email):
        """获取账户
        """
        async with self.async_dbsessionmaker.begin() as async_session:
            is_exist, account = await DBAccountOperater.get_account_by_email(session=async_session, email=email)
            return (True, Account.model_validate(account)) if is_exist else (False, None)

    async def authencicate_account(self, email: str, password: str):
        """校验账户
        """
        is_exist, account = await self.get_accounts_by_email(email)
        if not is_exist:
            return False, None
        if not self.verify_account(account, password):
            return False, None
        return True, account

    def delete_account(self, account: Account):
        """物理删除一个账户的所有信息。 
        """
        pass

    def make_account_access_token(self, account: Account, token_expire_minutes: int = 10, token_secret_key: str = "", token_algorithm=""):

        now_dt = datetime.now(timezone.utc) + \
            timedelta(minutes=token_expire_minutes)
        # TODO 加盐优化
        info = f"asdkfjkldsf#{account.account_name}#werdsfsdf#{str(now_dt)}"
        sub = hashlib.sha256(info.encode("utf8")).hexdigest()
        data = {
            "sub": sub,
            "exp": now_dt
        }
        encode_jwt = jwt.encode(data, str(token_secret_key),
                                algorithm=token_algorithm)

        return encode_jwt
