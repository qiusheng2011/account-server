from typing import Optional

from pydantic import (
    BaseModel
)
from sqlalchemy.orm import sessionmaker as SessionFactory

from .model import Account
from .dbmodel import DBAccount


class AccountManager():
    """账户管理器
    """
    def __init__(self, dbsessionmaker:Optional[SessionFactory]=None):
        self.dbsessionmaker = dbsessionmaker

    class config:
        arbitrary_types_allowed=True

    def register(self, account: Account):
        """注册一个账户
        """
        dbaccount = DBAccount(**account.model_dump(exclude_unset=True))
        with self.dbsessionmaker.begin() as session:
            session.add(dbaccount)

        return True

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
