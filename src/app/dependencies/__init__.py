from .database import orm, init_db_connect


def get_dbsessionmaker() -> orm.sessionmaker:
    from .database import DBSessionMaker
    return DBSessionMaker
