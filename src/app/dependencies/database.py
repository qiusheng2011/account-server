from sqlalchemy import (
    create_engine,
    orm,
    text
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

CONNECT_ARGS = {
    "connect_timeout": 5
}

DBSessionMaker = None


def init_db_connect_pool(url, connect_args=CONNECT_ARGS):
    global DBSessionMaker
    engine = create_engine(url, echo=True, connect_args=connect_args)
    SessionMaker = orm.sessionmaker(engine)
    DBSessionMaker = SessionMaker

# DBSessionMaker = init_db_connect(DB_CON_URL, CONNECT_ARGS)


AsyncDBsessionMaker = None


def init_async_db_connect_pool(url, connect_args=CONNECT_ARGS):
    global AsyncDBsessionMaker
    engine = create_async_engine(url, echo=True, connect_args=connect_args)
    AsyncDBsessionMaker = async_sessionmaker(bind=engine)
