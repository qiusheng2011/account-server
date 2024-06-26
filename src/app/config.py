import functools

import pydantic
import pydantic_settings
import pathlib


_CURRENT_DIR = str(pathlib.Path(__file__).parent)
APP_CONFIG_PREFIX = "account_server"


class AppConfig(pydantic_settings.BaseSettings):
    """ 配置
    """
    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix=f"{APP_CONFIG_PREFIX}_",
        case_sensitive=False,
        env_file=(".env", ".env.prod", ".env.dev"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

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
    log_dir: pydantic.DirectoryPath | None = pathlib.Path(
        f"{_CURRENT_DIR}/../../../")
    log_prefix: str = APP_CONFIG_PREFIX

    log_server_url: pydantic.AnyUrl | None = None
    # DB
    mysql_dsn: pydantic.MySQLDsn = pydantic.Field(default=None)
    mysql_connect_args: dict | None = {
        "connect_timeout": 2
    }

    # redis
    redis_dsn: pydantic.RedisDsn = pydantic.Field(default=None)
    redis_connect_timeout_s: int = 2

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
        """ log文件完整路径
        """
        if self.log_dir:
            return f"{self.log_dir.absolute()}/{self.log_prefix}_{self.port}"
        else:
            return ""


_APP_CONFIG: AppConfig | None = None


def get_app_config() -> AppConfig:
    """获取配置
    """
    global _APP_CONFIG
    if not _APP_CONFIG:
        _APP_CONFIG = AppConfig()
    return _APP_CONFIG
