from .database import DBSessionMaker, orm

def get_dbsessionmaker() -> orm.sessionmaker:
    return DBSessionMaker