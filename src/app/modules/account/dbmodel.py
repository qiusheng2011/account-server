
from datetime import datetime
from sqlalchemy import (
    orm,
    String,
    TIMESTAMP
)

class Base(orm.DeclarativeBase):
    pass

class DBAccount(Base):
    __tablename__ = "accounts"

    aid:orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email:orm.Mapped[str] = orm.mapped_column(String(50))
    account_name:orm.Mapped[str] = orm.mapped_column(String(20))
    hash_password:orm.Mapped[str] = orm.mapped_column(String(64))
    register_time:orm.Mapped[datetime] = orm.mapped_column(TIMESTAMP)
