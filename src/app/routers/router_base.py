from typing import Optional

from pydantic import (
    BaseModel
)


class BaseReponseModel(BaseModel):

    status: int = 0
    message: str = "ok"
    rst: Optional[dict] = {}


class Token(BaseModel):
    access_token: str
    token_type: str
    expire_in: int
    refresh_token: str
    refresh_token_expire_in: int
