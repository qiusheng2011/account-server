from typing import Optional
from pydantic import (
    MySQLDsn,
    Field,
    IPvAnyAddress,
    SecretStr,
    computed_field
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

    # token settings
    access_token_expire_minutes: int = 60
    token_secret_key: SecretStr = Field(
        default="94ebf1893ee9491c50c74a4e55ab14b1610b371de4f8c10f04955e812f9bafbd")
    token_algorithm: str = "HS256"

    # DB
    mysql_dsn: MySQLDsn = Field(default=None)
    mysql_connect_args: Optional[dict] = Field(default=None)

    model_config = SettingsConfigDict(
        env_prefix=f"{APP_CONFIG_PREFIX}_",
        case_sensitive=False
    )

    @computed_field
    def access_token_expire_seconds(self) -> int:
        return self.access_token_expire_minutes*60


appconfig = None


def setting_app_config() -> AppConfig:
    global appconfig
    appconfig = AppConfig()
    return appconfig
