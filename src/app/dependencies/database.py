
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

CONNECT_ARGS = {
    "connect_timeout": 5
}

AsyncDBsessionMaker = None


def init_async_db_connect_pool(url, connect_args=CONNECT_ARGS, debug=False):
    global AsyncDBsessionMaker
    engine = create_async_engine(
        url,
        echo=debug,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_timeout=10
    )
    AsyncDBsessionMaker = async_sessionmaker(bind=engine)
