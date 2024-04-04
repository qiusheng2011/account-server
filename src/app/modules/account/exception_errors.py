

class AccountExistError(Exception):
    """注册账户时，账户已存在"""

    def __init__(self):
        super().__init__("账户已存在无法注册,请修改邮箱或者用户名")


class AccountUnactivateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("账户已注册,但未激活", *args)


class AccountActivationNotFoundError(Exception):
     def __init__(self):
        super().__init__("无法获取激活信息")

class AccountActivationHasUsedError(Exception):
     def __init__(self):
        super().__init__("已经被激活过")