import uvicorn
from fastapi import FastAPI

from .routers import account

from .config import appconfig
from .dependencies import  init_db_connect


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

appserver.config = appconfig
init_db_connect(appconfig.mysql_dsn.unicode_string())

appserver.include_router(account.account_router)


@appserver.get("/", tags=["ServerHealth"])
def root():
    return {"message": "account appserver!"}


@appserver.get("/health", tags=["ServerHealth"])
def health():
    return
