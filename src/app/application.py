""" application server
"""

from fastapi import FastAPI
from fastapi.middleware import cors as fastapi_cors

from src.app.routers import account
from src.app import logging_config
from src.app import config
from src.app import dependencies


app_description = """
这一个独立的账户服务。
提供登陆和注册的相关账户功能。
其它服务不应当实现账户功能而是通过此服务获得 相应的账户id信息。
"""


appserver = FastAPI(
    title="AccountAppServer(账号服务)",
    description=app_description,
    version="0.0.1",
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
)
appserver.add_middleware(
    fastapi_cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 配置
app_config = config.get_app_config()
appserver.extra = {}
appserver.extra.setdefault("config", app_config)

# 日志配置
logging_config.seting_logging_config(
    server_name=app_config.server_name,
    logfile_path=app_config.log_path,
    debug=app_config.debug,
    log_server_url=app_config.log_server_url)

# 数据库初始化
dependencies.init_async_db_connect_pool(
    str(app_config.mysql_dsn), debug=app_config.debug)

# redis event_db_pool
dependencies.init_async_event_db_connect_pool(
    str(app_config.redis_dsn),
    connect_timeout_s=app_config.redis_connect_timeout_s
    )

# 导入API路由
appserver.include_router(account.account_router)


@appserver.get("/", tags=["ServerHealth"], include_in_schema=False)
async def root():
    """根路径
    """
    return {"message": "account appserver!"}


@appserver.get("/health", tags=["ServerHealth"], include_in_schema=False)
async def health():
    """健康检查
    """
    return {"status": 0, "message": "ok"}
