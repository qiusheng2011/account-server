
import re
import logging

from fastapi import (
    APIRouter,
    Form,
    Depends,
    Response,
    security,
    HTTPException,
    Request,
)
from pydantic import BaseModel
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import async_sessionmaker


from ..dependencies import get_dbsessionmaker, get_async_dbsessionmaker
from ..tool.tool import get_hash_password
from ..modules.account import (
    get_account_manager,
    Account,
    AccountManager,
    AccountExistError
)
from .router_base import BaseReponseModel, Token
from .exception import (
    PasswordIllegalHTTPException,
    AuthenticateUserFailed,
    AuthenticateFailed,
    AuthenricateRefreshTokenError
)

oauth2_schema = security.OAuth2PasswordBearer(tokenUrl="/v2/authorization")
account_router = APIRouter(prefix="/account", tags=["account"])
logger = logging.getLogger(__name__)



email_pattern = r"^[a-zA-Z0-9.+-_%]+@[a-zA-Z0-9.+-_%]+\.[a-zA-Z]{2,50}$"
password_pattern = r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*[a-z])(?=.*[A-Z]).{8,16}$"
account_name_pattern = r"[a-zA-Z0-9\u4E00-\u9FFF]{2,20}"


@account_router.post("/register", response_model=BaseReponseModel)
async def account_register(email: str = Form(pattern=email_pattern),
                           account_name: str = Form(
                               pattern=account_name_pattern),
                           password: str = Form(pattern=r".{8,16}"),
                           dbsessionmaker: callable = Depends(
                               get_async_dbsessionmaker)
                           ):
    """ 账户注册
    """
    try:
        account_manager: AccountManager = get_account_manager(dbsessionmaker)
        if not re.match(password_pattern, password):
            raise PasswordIllegalHTTPException()
        new_account = Account(
            email=email,
            account_name=account_name,
            hash_password=get_hash_password(password)
        )
        await account_manager.register(new_account)
    except AccountExistError as ex:
        return {
            "status": 4,
            "message": str(ex)
        }

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
async def signin(request: Request, form_data: security.OAuth2PasswordRequestForm = Depends(),
                 dbsessionmaker: async_sessionmaker = Depends(
    get_async_dbsessionmaker)
) -> Token:
    account_manager = get_account_manager(dbsessionmaker)
    is_exist, account = await account_manager.authencicate_account(form_data.username, form_data.password)
    if not is_exist:
        raise AuthenticateUserFailed()
    config = request.app.extra.get("config", None)
    access_token, refresh_token, start_timestamp = await account_manager.make_account_access_token(
        account,
        token_expire_minutes=config.access_token_expire_minutes,
        token_secret_key=config.token_secret_key,
        token_algorithm=config.token_algorithm,
        refresh_token_expire_extra_minutes=config.refresh_token_expire_extra_minutes
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expire_in=config.access_token_expire_seconds + start_timestamp,
        refresh_token=refresh_token,
        refresh_token_expire_in=config.refresh_token_expire_seconds + start_timestamp
    )


class ERTRequestModel(BaseModel):
    grant_type: str = Form()
    refresh_token: str = Form()


@account_router.post("/v2/accesstoken")
async def exchange_refresh_token(request: Request, form_data: ERTRequestModel = Depends(),
                                 dbsessionmaker: async_sessionmaker = Depends(get_async_dbsessionmaker)):
    if form_data.grant_type != "refresh_token":
        raise HTTPException(
            status_code=400, detail="The provided authorization grant or refresh token is invalid, expired or revoked")
    account_manager = AccountManager(dbsessionmaker)
    is_exist, account = await account_manager.authencicate_account_by_refresh_token(form_data.refresh_token)
    if not is_exist:
        raise AuthenricateRefreshTokenError()
    config = request.app.extra.get("config", None)
    access_token, refresh_token, start_timestamp = await account_manager.make_account_access_token(
        account,
        token_expire_minutes=config.access_token_expire_minutes,
        token_secret_key=config.token_secret_key,
        token_algorithm=config.token_algorithm,
        refresh_token_expire_extra_minutes=config.refresh_token_expire_extra_minutes
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expire_in=config.access_token_expire_seconds + start_timestamp,
        refresh_token=refresh_token,
        refresh_token_expire_in=config.refresh_token_expire_seconds + start_timestamp
    )

async def get_activate_account(request: Request, token: str = Depends(oauth2_schema), dbsessionmaker: async_sessionmaker = Depends(
        get_async_dbsessionmaker)):
    account_manager = AccountManager(dbsessionmaker)
    config = request.app.extra.get("config", None)
    account = await account_manager.get_account_by_token(
        token,
        token_secret_key=config.token_secret_key,
        token_algorithm=config.token_algorithm
    )

    if not account:
        raise AuthenticateFailed()
    else:
        return account


async def get_current_account(account=Depends(get_activate_account)):
    if not account:
        raise AuthenticateFailed()
    else:
        return account


@account_router.get("/token")
def checking_token(account: Account = Depends(get_current_account)):
    return {
        "aid":account.aid,
        "account_name": account.account_name
    }


@account_router.get("/me")
def get_me_account(account: Account = Depends(get_current_account)):
    return {
        "account_name": account.account_name
    }
