"""(异步并发)邮件发送监听
"""
from urllib import parse
import time
import asyncio
import datetime
import logging
from typing import Optional
import smtplib
from email.mime import text as email_text
from email.mime import multipart as email_multipart
import functools

from redis import asyncio as asyncio_redis
import pydantic
import pydantic_settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WORKER_CONFIG_PREFIX = "account_worker"


def caculate_time_cost(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        s_t = time.time()*1000
        rst = f(*args, **kwargs)
        e_t = time.time()*1000
        cost = e_t - s_t
        print(f"{f.__name__}\tcost:{cost}ms")
        return rst
    return wrapper


class WorkerConfig(pydantic_settings.BaseSettings):
    """ 启动配置
    """

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix=f"{WORKER_CONFIG_PREFIX}_",
        env_file=(".env", ".env.prod", ".env.dev"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    task_nums: int = pydantic.Field(default=5, description="监听任务的线程数")

    redis_dsn: pydantic.RedisDsn = pydantic.Field(description="redis地址")

    # smtp 服务设置
    smtp_server_url: pydantic.AnyUrl = pydantic.Field(description="SMTP服务地址")
    smtp_from_mail: str = pydantic.Field(description="stmp发件人地址")

    account_activate_weburl_f: str = pydantic.Field(
        default="https://xxxx?activate_token={activate_token}",
        description="账户激活请求地址待格式化字符串（必须包含{activate_token}）"
    )


class Event(pydantic.BaseModel):
    """事件"""
    event_name: str
    event_time: datetime.datetime
    data: Optional[dict] = pydantic.Field(default_factory=dict)


class SmtpServer(pydantic.BaseModel):
    """邮件发送器"""

    url: str
    port: int = 587
    user: str
    password: str
    from_mail: str

    def send_email(self, to_email, subject, body):
        message = email_multipart.MIMEMultipart()
        message["from"] = self.from_mail
        message["to"] = to_email
        message["Subject"] = subject
        message.attach(email_text.MIMEText(body))

        try:
            with smtplib.SMTP(host=self.url, port=self.port) as server:
                server.starttls()
                server.login(
                    user=self.user,
                    password=self.password
                )

                server.send_message(message)
                logging.info(f"to-email:{to_email}>发送成功")
                return True
        except smtplib.SMTPAuthenticationError as ex:
            logging.error(str(ex))
            return False


class EmailSendWorker():
    """ 邮件发送监听器
    """
    channel_name = "account_server"

    def __init__(self, event_db_pool, smtp_server: SmtpServer, activate_web_url: str):
        self.event_db_pool = event_db_pool
        self.smtp_server = smtp_server
        self.activate_web_url = activate_web_url

    def make_account_activate_body(self, email, activate_token):
        activate_token_url = self.activate_web_url.format(
            activate_token=activate_token)
        body = (f"""
            Dear User({email}):\n
                click link for activate account:\n
                \n{activate_token_url}\n
            """)
        return body

    @caculate_time_cost
    def send_account_activate_email(self, register_success_event):
        account_email = register_success_event.data.get("account_email", None)
        account_aid = register_success_event.data.get("account_aid", None)
        activate_token = register_success_event.data.get(
            "activate_token", None)
        if not account_email or not account_aid or not activate_token:
            logger.error(
                f"event:{register_success_event.event_name}.data 无法获取 email 或者 aid 或者 activate_token")
            return False

        mail_body = self.make_account_activate_body(
            account_email, activate_token)
        send_ok = self.smtp_server.send_email(
            subject="Activate Account (in 24 hours)",
            body=mail_body,
            to_email=account_email
        )
        return send_ok

    async def run(self, send_mail_timeout=10):
        logger.info("worker start !")
        try:
            async with asyncio_redis.Redis.from_pool(self.event_db_pool) as async_redis:
                while True:
                    channel, event_str = await async_redis.brpop([self.channel_name])
                    logger.info(f"{channel}\t{event_str}")
                    event = Event.model_validate_json(
                        event_str) if event_str else None
                    try:
                        async with asyncio.timeout(send_mail_timeout):
                            success = await asyncio.to_thread(self.send_account_activate_email, event)
                    except TimeoutError:
                        logger.warning(
                            f"{channel}\t{event_str}\t\tsend_mail_timeout")

        except Exception as ex:
            logger.error(str(ex))


async def main():
    """ 运行函数
    """

    config = WorkerConfig()

    smtp_server = SmtpServer(
        url=config.smtp_server_url.host or "",
        port=config.smtp_server_url.port or 0,
        user=parse.unquote(config.smtp_server_url.username or ""),
        password=parse.unquote(config.smtp_server_url.password or ""),
        from_mail=config.smtp_from_mail
    )
    event_db_pool = asyncio_redis.ConnectionPool.from_url(
        str(config.redis_dsn))
    esw = EmailSendWorker(
        event_db_pool=event_db_pool,
        smtp_server=smtp_server,
        activate_web_url=config.account_activate_weburl_f
    )
    runners = []
    async with asyncio.TaskGroup() as tg:
        for i in range(config.task_nums or 1):
            runners.append(tg.create_task(esw.run(), name=f"runner_{i}"))


if __name__ == "__main__":
    asyncio.run(main())
