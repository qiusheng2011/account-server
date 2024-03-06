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
    or_,
    ForeignKey,
    PrimaryKeyConstraint
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

    token = orm.Relationship('DBAccountCertificateToken',
                             uselist=False, back_populates="account", lazy="joined")


class DBAccountCertificateToken(Base):
    __tablename__ = "accounts_certificate_token"

    aid: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('accounts.aid'), primary_key=True)
    token: orm.Mapped[str] = orm.mapped_column(unique=True)
    refresh_token: orm.Mapped[str] = orm.mapped_column(unique=True)

    account = orm.Relationship(
        'DBAccount', uselist=False, back_populates="token")


class DBAccountOperater():

    @staticmethod
    async def check_accout_by_email_and_account_name(session: AsyncSession, email: str, account_name: str) -> bool:
        try:
            subq = Select(DBAccount.aid).where(
                or_(DBAccount.email == email, DBAccount.account_name == account_name))
            result = await session.execute(subq)
            data = result.first()
            return True if data else False
        except Exception as ex:
            raise ex

    @staticmethod
    async def get_account_by_email(session: AsyncSession, email: str) -> Tuple[bool, Optional[DBAccount]]:
        try:
            selectsql = Select(DBAccount).where(DBAccount.email == email).limit(1)
            results = await session.execute(selectsql)
            account = results.scalar_one_or_none()
            return (True, account) if account else (False, None)
        except Exception as ex:
            raise ex

    @staticmethod
    async def get_account_by_refresh_token(session: AsyncSession, refresh_token: str):
        try:
            selectsql = Select(DBAccount).where(
                DBAccountCertificateToken.refresh_token == refresh_token)
            results = await session.execute(selectsql)
            account = results.scalar_one_or_none()
            return (True, account) if account else (False, None)
        except Exception as ex:
            raise ex

    @staticmethod
    async def save_account_token(sesssion: AsyncSession, account_token: DBAccountCertificateToken):
        try:
            await sesssion.merge(account_token)
        except Exception as ex:
            raise ex

    @staticmethod
    async def get_account_by_token(session: AsyncSession, token: str) -> Optional[DBAccount]:
        try:
            sql = Select(DBAccountCertificateToken).options(orm.selectinload(DBAccountCertificateToken.account)).where(
                DBAccountCertificateToken.token == token).limit(1)
            results = await session.execute(sql)
            dbac_token = results.scalar_one_or_none()
            dbaccount = dbac_token.account if dbac_token else None
            return dbaccount if dbaccount else None
        except Exception as ex:
            raise ex
