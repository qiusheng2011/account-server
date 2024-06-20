
from sqlalchemy.ext import asyncio as asyncio_sa
from redis import asyncio as asyncio_redis

CONNECT_ARGS = {
    "connect_timeout": 5
}

AsyncDBSessionMaker = None


def init_async_db_connect_pool(url, connect_args=CONNECT_ARGS, debug=False):
    global AsyncDBSessionMaker
    engine = asyncio_sa.create_async_engine(
        url,
        echo=debug,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_timeout=10
    )
    AsyncDBSessionMaker = asyncio_sa.async_sessionmaker(
        autoflush=True, bind=engine)


event_db_pool = None


def init_async_event_db_connect_pool(url, connect_timeout_s=2):
    global event_db_pool
    event_db_pool = asyncio_redis.ConnectionPool.from_url(url=url, socket_connect_timeout=connect_timeout_s)
