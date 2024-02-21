from sqlalchemy import (
    create_engine,
    orm,
    text
)

DB_CON_URL = "mysql+pymysql://tts:askdjflwe234kjkjlr2332f@192.168.196.86/tts"
CONNECT_ARGS = {
    "connect_timeout": 1
}

DBSessionMaker = None

def init_db_connect(url, connect_args=CONNECT_ARGS):
    global DBSessionMaker
    engine = create_engine(url, echo=True, connect_args=connect_args)
    SessionMaker = orm.sessionmaker(engine)
    DBSessionMaker = SessionMaker

# DBSessionMaker = init_db_connect(DB_CON_URL, CONNECT_ARGS)
