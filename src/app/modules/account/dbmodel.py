from typing import (
    Optional,
    Tuple
)
from datetime import datetime
from sqlalchemy import (
    orm,
    String,
    TIMESTAMP,
    Select,
    or_
)
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession


class Base(AsyncAttrs, orm.DeclarativeBase):
    pass


class DBAccount(Base):
    __tablename__ = "accounts"

    aid: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(String(50))
    account_name: orm.Mapped[str] = orm.mapped_column(String(20))
    hash_password: orm.Mapped[str] = orm.mapped_column(String(64))
    register_time: orm.Mapped[datetime] = orm.mapped_column(TIMESTAMP)


class DBAccountOperater():

    @staticmethod
    async def check_accout_by_email_and_account_name(session: AsyncSession, email: str, account_name: str) -> bool:
        subq = Select(DBAccount.aid).where(
            or_(DBAccount.email == email, DBAccount.account_name == account_name))
        result = await session.execute(subq)
        data = result.first()
        return True if data else False

    @staticmethod
    async def get_account_by_email(session: AsyncSession, email: str) -> Tuple[bool, Optional[DBAccount]]:
        selectsql = Select(DBAccount).where(DBAccount.email == email).limit(1)
        results = await session.execute(selectsql)
        account = results.scalar_one()
        return (True, account) if account else (False, None)
