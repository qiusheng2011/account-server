import os
import secrets
import datetime

from redis import asyncio as asyncio_redis
import pytest
from sqlalchemy.ext import asyncio as sa_asyncio

from src.app.modules.account import account_manage
from src.app.modules.account import model
from src.app.modules.account import dbmodel
from src.app.tool import tool

REDIS_DSN_KEY = "account_server_test_redis_dsn"


class TestClassAccountManage:

    redis_dsn = os.getenv(REDIS_DSN_KEY) or os.getenv(REDIS_DSN_KEY.upper())

    # def on_start(self):
    #     self.redis_dsn = os.getenv(
    #         REDIS_DSN_KEY) or os.getenv(REDIS_DSN_KEY.upper())
    #     assert self.redis_dsn, f"环境变量({REDIS_DSN_KEY} or {
    #         REDIS_DSN_KEY.upper()})无法获取."

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

    @pytest.fixture(scope="session")
    def event_db_pool_obj(self):
        assert self.redis_dsn
        event_db_pool = asyncio_redis.ConnectionPool.from_url(self.redis_dsn)
        return event_db_pool

    @pytest.fixture(scope="session")
    def account_manage_obj(self, sessionmaker, event_db_pool_obj) -> account_manage.AccountManager:
        return account_manage.AccountManager(sessionmaker, event_db_pool_obj)

    async def test_register(self, account_manage_obj):

        # 创建用户
        time_mark = int(datetime.datetime.now().timestamp()*1000)
        activate_token = secrets.token_urlsafe()
        account = model.Account(
            email=f"test_account_manage_{time_mark}@test.test",
            account_name=f"test_am_{time_mark}",
            hash_password=tool.get_hash_password("sadkfjekwjrekwlrj32")
        )
        register_ok = await account_manage_obj.register(account, activate_token)
        assert register_ok
        assert account.aid

        activate_ok = await account_manage_obj.activate_account(activate_token)
        assert activate_ok
        delete_ok = await account_manage_obj.delete_account(account)
        assert delete_ok
