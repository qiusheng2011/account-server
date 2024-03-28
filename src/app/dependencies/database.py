
from sqlalchemy.ext import asyncio as sa_asyncio

CONNECT_ARGS = {
    "connect_timeout": 5
}

AsyncDBsessionMaker = None


def init_async_db_connect_pool(url, connect_args=CONNECT_ARGS, debug=False):
    global AsyncDBsessionMaker
    engine = sa_asyncio.create_async_engine(
        url,
        echo=debug,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_timeout=10
    )
    AsyncDBsessionMaker = sa_asyncio.async_sessionmaker(autoflush=True, bind=engine)
