from .database import (
    async_sessionmaker,
    init_async_db_connect_pool # 外部使用
)

from sqlalchemy import orm

def get_dbsessionmaker() -> orm.sessionmaker:
    """

    Returns:
        orm.sessionmaker: _description_
    """
    from .database import DBSessionMaker
    return DBSessionMaker


def get_async_dbsessionmaker() -> async_sessionmaker:
    """异步IO async session maker

    Returns:
        async_sessionmaker: _description_
    """
    from .database import AsyncDBsessionMaker
    return AsyncDBsessionMaker
