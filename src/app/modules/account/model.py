from typing import Optional
from pydantic import (
    BaseModel,
    Field
)


class AccountToken(BaseModel):

    token: str = ""
    refresh_token: str = ""

    class Config:
        from_attributes = True


class Account(BaseModel):

    aid: Optional[int] = Field(default=None, title="账户id")
    email: str = Field(title="邮箱")
    account_name: str = Field(title="账户名")
    hash_password: str = Field(title="hash密码")
    token: Optional[AccountToken] = None

    class Config:
        from_attributes = True

    def verfiy(self):
        """验证账户
        """
        pass

    def make_accecss_token(self):
        """ 生成账户权限
        """
