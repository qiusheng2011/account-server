from typing import Union, Optional
from .model import (
    Account
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from redis import asyncio as asyncio_redis

from .account_manage import AccountManager
from .exception_errors import *


def get_account_manager(dbsessionmaker: async_sessionmaker, event_db_pool: Optional[asyncio_redis.ConnectionPool] = None) -> AccountManager:
    return AccountManager(dbsessionmaker, event_db_pool)
