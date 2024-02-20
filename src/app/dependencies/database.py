from sqlalchemy import (
    create_engine,
    orm,
    text
)

DB_CON_URL = "mysql+pymysql://tts:askdjflwe234kjkjlr2332f@192.168.196.86"
CONNECT_ARGS = {
    "connect_timeout":1,
    "db":"tts"
}

def init_db_connect(url, connect_args):

    engine = create_engine(url,echo=True, connect_args=connect_args)
    SessionMaker = orm.sessionmaker(engine)
    return SessionMaker

DBSessionMaker = init_db_connect(DB_CON_URL, CONNECT_ARGS)
