import datetime
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
            email:
            account_name:
            hash_passowrd:
    """

    aid: int | None = pydantic.Field(default=None, title="账户id")
    email: str = pydantic.Field(title="邮箱")
    account_name: str = pydantic.Field(title="账户名")
    hash_password: str = pydantic.Field(title="hash密码")
    activation: int = 0
    token: AccountToken | None = None

    class Config:
        from_attributes = True

    def verfiy(self):
        """验证账户
        """
        pass

    def make_accecss_token(self):
        """ 生成账户权限
        """


class AccountActivation(pydantic.BaseModel):

    aid: int
    activate_token: str
    expire_time: datetime.datetime
    used: bool = False
