from sqlalchemy.ext import asyncio as sa_asyncio
from sqlalchemy import orm
from redis import asyncio as asyncio_redis

from .database import (
    init_async_db_connect_pool,  # 外部使用
    init_async_event_db_connect_pool
)


def get_async_dbsessionmaker() -> sa_asyncio.async_sessionmaker:
    """异步IO async session maker

    Returns:
        async_sessionmaker: _description_
    """
    from .database import AsyncDBSessionMaker
    return AsyncDBSessionMaker


def get_async_event_db_pool() -> asyncio_redis.ConnectionPool:
    from .database import event_db_pool
    return event_db_pool
