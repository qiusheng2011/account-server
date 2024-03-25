import logging
from typing import (
    Optional,
    Tuple
)
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, orm.DeclarativeBase):
    pass


class DBAccount(Base):
    __tablename__ = "accounts"

    aid: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    account_name: orm.Mapped[str] = orm.mapped_column(sa.String(20))
    hash_password: orm.Mapped[str] = orm.mapped_column(sa.String(64))
    register_time: orm.Mapped[datetime] = orm.mapped_column(sa.TIMESTAMP)

    token = orm.Relationship("DBAccountCertificateToken",
                             uselist=False, back_populates="account", lazy="joined")


class DBAccountCertificateToken(Base):
    __tablename__ = "accounts_certificate_token"

    aid: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("accounts.aid"), primary_key=True)
    token: orm.Mapped[str] = orm.mapped_column(unique=True)
    refresh_token: orm.Mapped[str] = orm.mapped_column(unique=True)

    account = orm.Relationship(
        "DBAccount", uselist=False, back_populates="token")


class DBAccountOperater():

    async def check_accout_by_email_and_account_name(self, session: AsyncSession, email: str, account_name: str) -> bool:
        try:
            subq = sa.Select(DBAccount.aid).where(
                sa.or_(DBAccount.email == email, DBAccount.account_name == account_name))
            result = await session.execute(subq)
            data = result.first()
            return True if data else False
        except Exception as ex:
            logger.critical(str(ex))
            raise ex

    async def get_account_by_email(self, session: AsyncSession, email: str) -> Tuple[bool, Optional[DBAccount]]:
        try:
            selectsql = sa.Select(DBAccount).where(
                DBAccount.email == email).limit(1)
            results = await session.execute(selectsql)
            account = results.scalar_one_or_none()
            return (True, account) if account else (False, None)
        except Exception as ex:
            logger.critical(str(ex))
            raise ex

    async def get_account_by_refresh_token(self, session: AsyncSession, refresh_token: str):
        try:
            selectsql = sa.Select(DBAccount).where(
                DBAccountCertificateToken.refresh_token == refresh_token)
            results = await session.execute(selectsql)
            account = results.scalar_one_or_none()
            return (True, account) if account else (False, None)
        except Exception as ex:
            logger.critical(str(ex))
            raise ex

    async def save_account_token(self, sesssion: AsyncSession, account_token: DBAccountCertificateToken):
        try:
            await sesssion.merge(account_token)
        except Exception as ex:
            logger.critical(str(ex))
            raise ex

    async def get_account_by_token(self, session: AsyncSession, token: str) -> Optional[DBAccount]:
        try:
            sql = sa.Select(DBAccountCertificateToken).options(orm.selectinload(DBAccountCertificateToken.account)).where(
                DBAccountCertificateToken.token == token).limit(1)
            results = await session.execute(sql)
            dbac_token = results.scalar_one_or_none()
            dbaccount = dbac_token.account if dbac_token else None
            return dbaccount if dbaccount else None
        except Exception as ex:
            logger.critical(str(ex))
            raise ex
