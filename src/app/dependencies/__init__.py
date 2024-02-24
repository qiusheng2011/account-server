from .database import (
    orm,
    init_db_connect_pool,
    init_async_db_connect_pool,
    async_sessionmaker
)


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
