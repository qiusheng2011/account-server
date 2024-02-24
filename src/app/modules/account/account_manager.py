from typing import Optional

from pydantic import (
    BaseModel
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as AsyncSessionFactory,
    AsyncSession
)

from .model import Account
from .dbmodel import DBAccount, DBAccountOperater
from .exception import AccountExistError


class AccountManager():
    """账户管理器
    """

    def __init__(self, async_dbsessionmaker: AsyncSessionFactory):
        self.async_dbsessionmaker = async_dbsessionmaker

    async def register(self, account: Account):
        """注册一个账户
        """
        dbaccount = DBAccount(**account.model_dump(exclude_unset=True))
        async with self.async_dbsessionmaker.begin() as async_session:
            check_result = await DBAccountOperater.check_accout_by_email_and_account_name(async_session, dbaccount.email, dbaccount.account_name)
            if check_result:
                raise AccountExistError()
            async_session.add(dbaccount)
            await async_session.flush()
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
