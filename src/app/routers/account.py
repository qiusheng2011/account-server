
import re
import logging
from typing import (
    Optional
)

import fastapi
from fastapi import (
    security,
    requests
)
import pydantic
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio
from redis import asyncio as asyncio_redis

from src.app import dependencies
from src.app.tool import tool
from src.app.modules import account
from src.app.modules.account import account_manage
from src.app.routers import router_base
from src.app.routers import exception_errors as routers_exceptions
oauth2_schema = security.OAuth2PasswordBearer(tokenUrl="/v2/authorization")
account_router = fastapi.APIRouter(prefix="/account", tags=["account"])
logger = logging.getLogger(__name__)


email_pattern = r"^[a-zA-Z0-9.+-_%]+@[a-zA-Z0-9.+-_%]+\.[a-zA-Z]+$"
password_pattern = r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*[a-z])(?=.*[A-Z]).{8,16}$"
account_name_pattern = r"[a-zA-Z0-9\u4E00-\u9FFF]{2,20}"


@account_router.post("/register", response_model=router_base.BaseReponseModel)
async def account_register(
    email: str = fastapi.Form(pattern=email_pattern, max_length=50),
    account_name: str = fastapi.Form(pattern=account_name_pattern),
    password: str = fastapi.Form(pattern=r".{8,16}"),
    dbsessionmaker: callable = fastapi.Depends(
        dependencies.get_async_dbsessionmaker),
    event_db_pool: asyncio_redis.ConnectionPool = fastapi.Depends(
        dependencies.get_async_event_db_pool)
):
    """ 账户注册
    """
    try:
        account_manager: account_manage.AccountManager = account.get_account_manager(
            dbsessionmaker,
            event_db_pool
        )
        if not re.match(password_pattern, password):
            raise routers_exceptions.PasswordIllegal422HttpError()
        new_account = account.Account(
            email=email,
            account_name=account_name,
            hash_password=tool.get_hash_password(password)
        )
        await account_manager.register(new_account)
    except account.AccountExistError:
        raise routers_exceptions.AccountExisted409HttpError()
    except account.AccountUnactivateError:
        raise routers_exceptions.AccountUnactivate403HttpError()

    return {
        "status": 1,
        "message": "ok",
        "rst": {
            "email": new_account.email,
            "account_name": new_account.account_name,
            "aid": new_account.aid
        }
    }


@account_router.post("/v2/authorization")
async def signin(request: fastapi.Request,
                 form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
                 dbsessionmaker: sqlalchemy_asyncio.async_sessionmaker = fastapi.Depends(dependencies.get_async_dbsessionmaker)) -> Optional[router_base.Token]:
    account_manager = account.get_account_manager(dbsessionmaker)
    is_exist, account_u = await account_manager.authencicate_account(form_data.username, form_data.password)
    if not is_exist:
        raise routers_exceptions.AuthenticateUserFailed401HttpError()
    elif account_u:
        config = request.app.extra.get("config", None)
        access_token, refresh_token, start_timestamp = await account_manager.make_account_access_token(
            account_u,
            token_expire_minutes=config.access_token_expire_minutes,
            token_secret_key=config.token_secret_key,
            token_algorithm=config.token_algorithm,
            refresh_token_expire_extra_minutes=config.refresh_token_expire_extra_minutes
        )
        return router_base.Token(
            access_token=access_token,
            token_type="bearer",
            expire_in=config.access_token_expire_seconds + start_timestamp,
            refresh_token=refresh_token,
            refresh_token_expire_in=config.refresh_token_expire_seconds + start_timestamp
        )


class ERTRequestModel(pydantic.BaseModel):
    grant_type: str = fastapi.Form()
    refresh_token: str = fastapi.Form()


@account_router.post("/v2/accesstoken")
async def exchange_refresh_token(request: requests.Request, form_data: ERTRequestModel = fastapi.Depends(),
                                 dbsessionmaker: sqlalchemy_asyncio.async_sessionmaker = fastapi.Depends(dependencies.get_async_dbsessionmaker)):
    if form_data.grant_type != "refresh_token":
        raise fastapi.HTTPException(
            status_code=400, detail="The provided authorization grant or refresh token is invalid, expired or revoked")
    account_manager = account_manage.AccountManager(dbsessionmaker)
    is_exist, account_u = await account_manager.authencicate_account_by_refresh_token(form_data.refresh_token)
    if not is_exist:
        raise routers_exceptions.AuthenricateRefreshToken400HttpError()
    elif account_u:
        config = request.app.extra.get("config", None)
        access_token, refresh_token, start_timestamp = await account_manager.make_account_access_token(
            account_u,
            token_expire_minutes=config.access_token_expire_minutes,
            token_secret_key=config.token_secret_key,
            token_algorithm=config.token_algorithm,
            refresh_token_expire_extra_minutes=config.refresh_token_expire_extra_minutes
        )

        return router_base.Token(
            access_token=access_token,
            token_type="bearer",
            expire_in=config.access_token_expire_seconds + start_timestamp,
            refresh_token=refresh_token,
            refresh_token_expire_in=config.refresh_token_expire_seconds + start_timestamp
        )


async def get_activate_account(request: requests.Request, token: str = fastapi.Depends(oauth2_schema), dbsessionmaker: sqlalchemy_asyncio.async_sessionmaker = fastapi.Depends(
        dependencies.get_async_dbsessionmaker)):
    account_manager = account_manage.AccountManager(dbsessionmaker)
    config = request.app.extra.get("config", None)
    account = await account_manager.get_account_by_token(
        token,
        token_secret_key=config.token_secret_key,
        token_algorithm=config.token_algorithm
    )

    if not account:
        raise routers_exceptions.AuthenticateFailed401HttpError()
    else:
        return account


async def get_current_account(account=fastapi.Depends(get_activate_account)):
    if not account:
        raise routers_exceptions.AuthenticateFailed401HttpError()
    else:
        return account


@account_router.get("/token")
def checking_token(account: account.Account = fastapi.Depends(get_current_account)):
    return {
        "aid": account.aid,
        "account_name": account.account_name
    }


@account_router.delete("/me")
async def delete_me_account(
    account: account.Account = fastapi.Depends(get_current_account),
    dbsessionmaker: sqlalchemy_asyncio.async_sessionmaker
        = fastapi.Depends(dependencies.get_async_dbsessionmaker)
):
    """ 删除账户
    """
    account_manager = account_manage.AccountManager(dbsessionmaker)
    await account_manager.delete_account(account)
    return router_base.BaseReponseModel(rst={"aid": account.aid})


@account_router.get("/me")
async def get_me_account(account: account.Account = fastapi.Depends(get_current_account)):
    return {
        "account_name": account.account_name,
        "aid": account.aid
    }
