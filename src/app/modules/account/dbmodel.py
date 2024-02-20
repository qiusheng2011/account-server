from typing import (
    Optional
)
from datetime import datetime
from sqlalchemy import (
    orm,
    String,
    TIMESTAMP,
    Select,
    or_
)

class Base(orm.DeclarativeBase):
    pass

class DBAccount(Base):
    __tablename__ = "accounts"

    aid:orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email:orm.Mapped[str] = orm.mapped_column(String(50))
    account_name:orm.Mapped[str] = orm.mapped_column(String(20))
    hash_password:orm.Mapped[str] = orm.mapped_column(String(64))
    register_time:orm.Mapped[datetime] = orm.mapped_column(TIMESTAMP)



class DBAccountOperater():

    
    @staticmethod
    def check_accout_by_email_and_account_name(session:orm.Session, email:str, account_name:str) -> Optional[int]:
        result = session.execute(Select(DBAccount.aid).where(or_(DBAccount.email==email,DBAccount.account_name==account_name)))
        account = result.fetchone()
        return None if not account else account[0]
