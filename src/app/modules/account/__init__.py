from typing import Union
from .model import (
    Account
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from .account_manage import AccountManager
from .exceptions import *


def get_account_manager(dbsessionmaker: async_sessionmaker) -> AccountManager:
    return AccountManager(dbsessionmaker)
