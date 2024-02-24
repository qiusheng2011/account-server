import time
import asyncio

import uvicorn
from fastapi import FastAPI

from .routers import account
from .config import setting_app_config
from .dependencies import (
    init_db_connect_pool,
    init_async_db_connect_pool
)


app_description = """
这一个独立的账户服务。\n
提供登陆和注册的相关账户功能。\n
其它服务不应当实现账户功能而是通过此服务获得 相应的账户id信息。

"""


appserver = FastAPI(
    title="AccountAppServer(账号服务)",
    description=app_description,
    version='0.0.1',
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
)

appserver.config = setting_app_config()
init_async_db_connect_pool(appserver.config.mysql_dsn.unicode_string())


appserver.include_router(account.account_router)


@appserver.get("/", tags=["ServerHealth"],include_in_schema=False)
async def root():
    return {"message": "account appserver!"}


@appserver.get("/health", tags=["ServerHealth"], include_in_schema=False)
async def health():
    return {"status":0, "message":"ok"}
