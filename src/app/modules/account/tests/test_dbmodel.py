import pytest
from sqlalchemy.ext import asyncio as sa_asyncio

from src.app.modules.account import dbmodel


class TestClassDBmodel:

    @pytest.fixture(scope="session")
    async def sessionmaker(self):
        engine = sa_asyncio.create_async_engine(
            url="sqlite+aiosqlite:///:memeory:",
            echo=True,
            pool_pre_ping=True
        )
        async with engine.begin() as conn:
            await conn.run_sync(dbmodel.Base.metadata.create_all)
        return sa_asyncio.async_sessionmaker(autoflush=True, bind=engine)

    async def test_delete_account(self, sessionmaker):

        db_account_opterator = dbmodel.DBAccountOperater()
        async with sessionmaker() as async_session:
            account = dbmodel.DBAccount(
                email="test@test.com",
                account_name="test",
                hash_password="0"*16,

            )
            async_session.add(account)
            await async_session.flush()
            aid = await db_account_opterator.delete_dbaccount(async_session, account)
            assert account.aid == aid
