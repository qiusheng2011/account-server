import logging
from typing import (
    Optional,
    Tuple
)
import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import func

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, orm.DeclarativeBase):
    pass


class DBAccount(Base):
    __tablename__ = "accounts"

    aid: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    account_name: orm.Mapped[str] = orm.mapped_column(sa.String(50))
    hash_password: orm.Mapped[str] = orm.mapped_column(sa.String(64))
    register_time: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.TIMESTAMP, default=func.now())
    activation: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=0)

    token = orm.Relationship("DBAccountCertificateToken",
                             uselist=False,
                             back_populates="account",
                             lazy="joined",
                             cascade="all, delete"
                             )


class DBAccountCertificateToken(Base):
    __tablename__ = "accounts_certificate_token"

    aid: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("accounts.aid", ondelete="cascade", onupdate="cascade"),
        primary_key=True)
    token: orm.Mapped[str] = orm.mapped_column(unique=True)
    refresh_token: orm.Mapped[str] = orm.mapped_column(unique=True)

    account = orm.Relationship("DBAccount",
                               uselist=False,
                               back_populates="token"
                               )


class DBAccountActivation(Base):
    __tablename__ = "account_activation"

    aid: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("accounts.aid",
                      ondelete="cascade",
                      onupdate="cascade",
                      ),
        primary_key=True
    )
    activate_token: orm.Mapped[str] = orm.mapped_column(unique=True)
    expire_time: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.TIMESTAMP)
    used: orm.Mapped[bool] = orm.mapped_column(sa.Integer, default=0)

    account = orm.Relationship("DBAccount",
                               uselist=False, lazy="joined")


class DBAccountOperater():

    async def check_accout_by_email_and_account_name(self, session: AsyncSession, email: str, account_name: str) -> tuple[bool, Optional[DBAccount]]:
        try:
            subq = sa.Select(DBAccount).where(
                sa.or_(DBAccount.email == email, DBAccount.account_name == account_name))
            result = await session.execute(subq)
            data = result.scalar_one_or_none()
            return (True, data) if data else (False, None)
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def get_account_by_email(self, session: AsyncSession, email: str) -> Tuple[bool, Optional[DBAccount]]:
        try:
            selectsql = sa.Select(DBAccount).where(
                sa.and_(DBAccount.email == email, DBAccount.activation == 1)).limit(1)
            results = await session.execute(selectsql)
            account = results.scalar_one_or_none()
            return (True, account) if account else (False, None)
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def get_account_by_aid(self, session: AsyncSession, aid: int | None) -> tuple[bool, DBAccount | None]:
        account = await session.get_one(DBAccount, aid)
        return (True if (account and account.activation == 1) else False), account

    async def get_account_by_refresh_token(self, session: AsyncSession, refresh_token: str):
        try:
            selectsql = sa.Select(DBAccount).where(
                DBAccountCertificateToken.refresh_token == refresh_token)
            results = await session.execute(selectsql)
            account = results.fetchone()
            return (True, account[0]) if account else (False, None)
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def save_account_token(self, sesssion: AsyncSession, account_token: DBAccountCertificateToken):
        try:
            await sesssion.merge(account_token)
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def get_account_activation(self, session: AsyncSession, activate_token):
        try:
            select_sql = sa.Select(DBAccountActivation).where(
                DBAccountActivation.activate_token == activate_token)
            results = await session.execute(select_sql)
            account_activation = results.scalar_one_or_none()
            return account_activation
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def accont_activate(self, session: AsyncSession, db_account_activation):
        try:
            db_account_activation.used = True
            db_account = db_account_activation.account
            db_account.activation = 1
            await session.commit()
            return True
        except Exception as ex:
            logger.error(str(ex))
            raise ex

    async def save_account_activation(self, session: AsyncSession, account_activation: DBAccountActivation):
        try:
            await session.merge(account_activation)
            return True
        except Exception as ex:
            logger.error(str(ex))
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
            logger.error(str(ex))
            raise ex

    async def delete_dbaccount(self, session: AsyncSession, account: DBAccount):
        """ 物理删除用户
        """
        try:
            await session.delete(account)
            return account.aid
        except Exception as ex:
            logger.error(str(ex))
            raise ex
