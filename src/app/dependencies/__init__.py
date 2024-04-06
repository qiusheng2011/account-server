from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import orm
from redis import asyncio as asyncio_redis

from .database import (
    init_async_db_connect_pool,  # 外部使用
    init_async_event_db_connect_pool
)


def get_async_dbsessionmaker() -> async_sessionmaker:
    """异步IO async session maker

    Returns:
        async_sessionmaker: _description_
    """
    from .database import AsyncDBsessionMaker
    return AsyncDBsessionMaker


def get_async_event_db_pool() -> asyncio_redis.ConnectionPool:
    from .database import event_db_pool
    return event_db_pool
