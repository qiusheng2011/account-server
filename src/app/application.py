
from fastapi import FastAPI

from app.routers import account
from app import logging_config
from app import config
from app import dependencies


app_description = """
这一个独立的账户服务。
提供登陆和注册的相关账户功能。
其它服务不应当实现账户功能而是通过此服务获得 相应的账户id信息。
"""


appserver = FastAPI(
    title="AccountAppServer(账号服务)",
    description=app_description,
    version='0.0.1',
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
)
app_config = config.get_app_config()
appserver.extra = {}
appserver.extra.setdefault('config', app_config)

# 异常注册

# 日志配置
logging_config.seting_logging_config(
    server_name=app_config.server_name,
    logfile_path=app_config.log_path,
    debug=app_config.debug,
    log_server_url=app_config.log_server_url
)
dependencies.init_async_db_connect_pool(
    str(app_config.mysql_dsn), debug=app_config.debug)


appserver.include_router(account.account_router)


@appserver.get("/", tags=["ServerHealth"], include_in_schema=False)
async def root():
    return {"message": "account appserver!"}


@appserver.get("/health", tags=["ServerHealth"], include_in_schema=False)
async def health():
    return {"status": 0, "message": "ok"}
