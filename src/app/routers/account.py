
import re
from fastapi import (
    APIRouter,
    Form,
    Depends
)
from sqlalchemy import orm

from ..dependencies import get_dbsessionmaker
from ..tool.tool import get_hash_password

from ..modules.account import (
    get_account_manager,
    Account,
    AccountManager,
    AccountExistError
)
from .router_base import BaseReponseModel


account_router = APIRouter(prefix="/account", tags=["account"])

email_pattern = r"^[a-zA-Z0-9.+-_%]+@[a-zA-Z0-9.+-_%]+\.[a-zA-Z]{2,50}$"
password_pattern = r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*[a-z])(?=.*[A-Z]).{8,16}$"
account_name_pattern = r".{2,20}"



@account_router.post("/register", response_model=BaseReponseModel)
def account_register(email: str = Form(pattern=email_pattern), 
                     account_name: str = Form(pattern=account_name_pattern),
                     password: str = Form(pattern=r".{8,16}")):
    """ 账户注册
    """
    try:
        account_manager:AccountManager=get_account_manager(get_dbsessionmaker())
        if not re.match(password_pattern, password):
            raise ValueError("密码不符合规范")
        new_account = Account(
            email=email,
            account_name=account_name,
            hash_password=get_hash_password(password)
        )
        account_manager.register(new_account)
    except AccountExistError as ex:
        return {
            "status":4,
            "message":str(ex)
        }

    return {
        "status": 1,
        "message": "ok",
        "rst":{
            "email": new_account.email,
            "account_name":new_account.account_name,
            "aid": new_account.aid
        }
    }
