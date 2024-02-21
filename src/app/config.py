from typing import Optional
from pydantic import (
    MySQLDsn,
    Field
)
from pydantic_settings import (
    BaseSettings
)


APP_CONFIG_PREFIX = "account_server"


class AppConfig(BaseSettings):

    mysql_dsn: MySQLDsn = Field(alias=F"{APP_CONFIG_PREFIX}_mysql_dsn")
    mysql_connect_args:Optional[dict] = Field(
        default=None, alias=F"{APP_CONFIG_PREFIX}_mysql_connect_args")


appconfig = AppConfig()
