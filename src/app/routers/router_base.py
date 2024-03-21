
from pydantic import (
    BaseModel
)


class BaseReponseModel(BaseModel):

    status: int = 0
    message: str = "ok"
    rst: dict | None = {}


class Token(BaseModel):
    access_token: str
    token_type: str
    expire_in: int
    refresh_token: str
    refresh_token_expire_in: int
