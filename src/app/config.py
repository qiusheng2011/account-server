from typing import Optional
from pydantic import (
    MySQLDsn,
    Field,
    IPvAnyAddress
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


APP_CONFIG_PREFIX = "account_server"


class AppConfig(BaseSettings):

    # server
    host: IPvAnyAddress = Field(default="127.0.0.1")
    port: int = Field(default=8700)

    workers: int = Field(default=1)
    # DB
    mysql_dsn: MySQLDsn = Field(default=None)
    mysql_connect_args: Optional[dict] = Field(default=None)

    model_config = SettingsConfigDict(env_prefix=f"{APP_CONFIG_PREFIX}_")



appconfig = None


def setting_app_config() -> AppConfig:
    global appconfig
    appconfig = AppConfig()
    return appconfig
