from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import orm

from .database import (
    init_async_db_connect_pool  # 外部使用
)


def get_async_dbsessionmaker() -> async_sessionmaker:
    """异步IO async session maker

    Returns:
        async_sessionmaker: _description_
    """
    from .database import AsyncDBsessionMaker
    return AsyncDBsessionMaker
