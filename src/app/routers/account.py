
import re
from datetime import timedelta

from fastapi import (
    APIRouter,
    Form,
    Depends,
    Response,
    security,
    HTTPException,
    Request
)
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
    AuthenticateUserFailed
)


account_router = APIRouter(prefix="/account", tags=["account"])


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


@account_router.post("/signin")
async def signin(request: Request, form_data: security.OAuth2PasswordRequestForm = Depends(),
                        dbsessionmaker: async_sessionmaker = Depends(
                            get_async_dbsessionmaker)
                        ) -> Token:
    account_manager = get_account_manager(dbsessionmaker)
    is_exist, account = await account_manager.authencicate_account(form_data.username, form_data.password)
    if not is_exist:
        raise AuthenticateUserFailed()
    access_token = account_manager.make_account_access_token(
        account, 
        token_expire_minutes=request.app.config.access_token_expire_minutes, 
        token_secret_key=request.app.config.token_secret_key,
        token_algorithm=request.app.config.token_algorithm
        )
    return Token(access_token=access_token, token_type="bearer")
