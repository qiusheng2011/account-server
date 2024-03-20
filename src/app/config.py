from typing import Optional
import functools

import pydantic
import pydantic_settings
import pathlib


CURRENT_DIR = str(pathlib.Path(__file__).parent)
APP_CONFIG_PREFIX = "account_server"


class AppConfig(pydantic_settings.BaseSettings):

    # server
    server_name: str = "account_server"
    host: pydantic.IPvAnyAddress = pydantic.Field(default="127.0.0.1")
    port: int = pydantic.Field(default=8700)
    debug: bool = False
    workers: int = pydantic.Field(default=1)

    # token settings
    access_token_expire_minutes: int = 60
    refresh_token_expire_extra_minutes: int = 1440
    token_secret_key: pydantic.SecretStr = pydantic.Field(
        default="94ebf1893ee9491c50c74a4e55ab14b1610b371de4f8c10f04955e812f9bafbd")
    token_algorithm: str = "HS256"

    # log
    log_dir: Optional[pydantic.DirectoryPath] = pathlib.Path(
        f"{CURRENT_DIR}/../../../logs/")
    log_prefix: str = APP_CONFIG_PREFIX

    log_server_url: Optional[pydantic.AnyUrl] = None

    # DB
    mysql_dsn: pydantic.MySQLDsn = pydantic.Field(default=None)
    mysql_connect_args: Optional[dict] = {
        "connect_timeout": 3
    }

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix=f"{APP_CONFIG_PREFIX}_",
        case_sensitive=False
    )

    @pydantic.computed_field
    @functools.cached_property
    def access_token_expire_seconds(self) -> int:
        return self.access_token_expire_minutes*60

    @pydantic.computed_field
    @functools.cached_property
    def refresh_token_expire_seconds(self) -> int:
        return self.access_token_expire_minutes*60 + self.refresh_token_expire_extra_minutes*60

    @pydantic.computed_field
    @functools.cached_property
    def log_path(self) -> str:
        if self.log_dir:
            return f"{self.log_dir.absolute()}/{self.log_prefix}_{self.port}"
        else:
            return ""


appconfig = None


def setting_app_config() -> AppConfig:
    global appconfig
    appconfig = AppConfig()
    return appconfig
