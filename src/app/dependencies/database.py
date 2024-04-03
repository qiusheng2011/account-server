
from sqlalchemy.ext import asyncio as asyncio_sa
from redis import asyncio as asyncio_redis

CONNECT_ARGS = {
    "connect_timeout": 5
}

AsyncDBsessionMaker = None


def init_async_db_connect_pool(url, connect_args=CONNECT_ARGS, debug=False):
    global AsyncDBsessionMaker
    engine = asyncio_sa.create_async_engine(
        url,
        echo=debug,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_timeout=10
    )
    AsyncDBsessionMaker = asyncio_sa.async_sessionmaker(
        autoflush=True, bind=engine)


event_db_pool = None


def init_async_event_db_connect_pool(url):
    global event_db_pool
    event_db_pool = asyncio_redis.ConnectionPool.from_url(url)
