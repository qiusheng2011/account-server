
from fastapi import (
    APIRouter,
    Form
)


account_router = APIRouter(prefix="/account", tags=["account"])

email_regex = r"^[a-zA-Z0-9.+-_%]+@[a-zA-Z0-9.+-_%]+\.[a-zA-Z]{2,}$"
password_regex = r"^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*[a-z])(?=.*[A-Z]).{8,16}$"
account_name = r".{2-20}"

@account_router.post("/register")
def account_register(email: str = Form(regex=email_regex), account_name: str = Form(),
                     password: str = Form(regex=password_regex)):
    pass
