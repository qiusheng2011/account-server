from .model import (
    Account
)
from fastapi import Depends
from sqlalchemy import orm

from .account_manager import AccountManager
from .exception import *



def get_account_manager(dbsessionmaker:orm.sessionmaker) -> AccountManager:
    return AccountManager(dbsessionmaker)
