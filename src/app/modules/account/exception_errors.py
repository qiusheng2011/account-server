

class AccountExistError(Exception):
    """注册账户时，账户已存在"""
    def __init__(self):
        super().__init__("账户已存在无法注册,请修改邮箱或者用户名")
