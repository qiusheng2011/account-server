from typing import Optional
import pydantic


class AccountToken(pydantic.BaseModel):

    token: str = ""
    refresh_token: str = ""

    class Config:
        from_attributes = True


class Account(pydantic.BaseModel):
    """ 账户

        attribute:
            aid:
            title:
            email:
            account_name:
            hash_passowrd:
    """

    aid: Optional[int] = pydantic.Field(default=None, title="账户id")
    email: str = pydantic.Field(title="邮箱")
    account_name: str = pydantic.Field(title="账户名")
    hash_password: str = pydantic.Field(title="hash密码")
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
