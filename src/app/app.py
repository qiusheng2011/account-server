import uvicorn
from fastapi import FastAPI

from .routers import account

app_description = """
这一个独立的账户服务。\n
提供登陆和注册的相关账户功能。\n
其它服务不应当实现账户功能而是通过此服务获得 相应的账户id信息。

"""


appserver = FastAPI(
    title="AccountAppServer",
    description=app_description,
    version='0.0.1',
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme":"monokai"},
)

appserver.include_router(account.account_router)



@appserver.get("/", tags=["ServerHealth"])
def root():
    return {"message":"account appserver!"}


@appserver.get("/health",tags=["ServerHealth"])
def health():
    return

