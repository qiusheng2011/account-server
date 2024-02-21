from typing import Optional

from pydantic import (
    BaseModel
)
from sqlalchemy.orm import sessionmaker as SessionFactory

from .model import Account
from .dbmodel import DBAccount, DBAccountOperater
from .exception import AccountExistError


class AccountManager():
    """账户管理器
    """

    def __init__(self, dbsessionmaker: SessionFactory):
        self.dbsessionmaker = dbsessionmaker

    class config:
        arbitrary_types_allowed = True

    def register(self, account: Account):
        """注册一个账户
        """
        dbaccount = DBAccount(**account.model_dump(exclude_unset=True))
        with self.dbsessionmaker.begin() as session:
            if DBAccountOperater.check_accout_by_email_and_account_name(session, dbaccount.email, dbaccount.account_name):
                raise AccountExistError()
            session.add(dbaccount)
            session.flush()
            account.aid = dbaccount.aid
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
