from pydantic import (
    BaseModel
)
from .model import Account


class AccountManager(BaseModel):
    """账户管理器
    """


    def register(self, account:Account):
       """注册一个账户
       """
       pass
    
    def verify_account(self, account: Account):
        """ 验证账户
        """
        pass 

    def get_accounts(self):
        """获取账户
        """
        pass

    def delete_account(self, account: Account):
        """物理删除一个账户的所有信息。 
        """
        pass
