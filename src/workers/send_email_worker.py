import sys
import os
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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

REDIS_DSN_KEY = "account_server_worker_redis_dsn"
REDIS_DSN = os.getenv(REDIS_DSN_KEY) or os.getenv(REDIS_DSN_KEY.upper())

SMTP_SERVER_USER_KEY = "account_server_worker_smtp_server_user"
SMTP_SERVER_USER = os.getenv(SMTP_SERVER_USER_KEY) or os.getenv(
    SMTP_SERVER_USER_KEY.upper())

SMTP_SERVER_PASSWORD_KEY = "account_server_worker_smtp_server_password"
SMTP_SERVER_PASSWORD = os.getenv(SMTP_SERVER_PASSWORD_KEY) or os.getenv(
    SMTP_SERVER_PASSWORD_KEY.upper())

ACTIVATE_WEB_URL_KEY = "account_server_worker_account_activate_weburl_f"
ACTIVATE_WEB_URL = os.getenv(ACTIVATE_WEB_URL_KEY) or os.getenv(
    ACTIVATE_WEB_URL_KEY.upper())

if not SMTP_SERVER_USER or not SMTP_SERVER_PASSWORD or not ACTIVATE_WEB_URL or not REDIS_DSN:
    raise ValueError(f"无法获取到环境变量 {SMTP_SERVER_USER_KEY} or {
                     SMTP_SERVER_PASSWORD} ")


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


class Event(pydantic.BaseModel):

    event_name: str
    event_time: datetime.datetime
    data: Optional[dict] = pydantic.Field(default_factory=dict)


class SmtpServer(pydantic.BaseModel):

    url: str = "smtp.mail.me.com"
    port: int = 587

    user: str
    password: str
    from_mail: str = "schoupdev@icloud.com"

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
            logging.critical(str(ex))
            return False


class EmailSendWorker():

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


async def main(task_nums=10):
    smtp_server = SmtpServer(
        user=SMTP_SERVER_USER,
        password=SMTP_SERVER_PASSWORD
    )
    event_db_pool = asyncio_redis.ConnectionPool.from_url(REDIS_DSN)
    esw = EmailSendWorker(
        event_db_pool=event_db_pool,
        smtp_server=smtp_server,
        activate_web_url=ACTIVATE_WEB_URL
    )
    runners = []
    async with asyncio.TaskGroup() as tg:
        for i in range(task_nums):
            runners.append(tg.create_task(esw.run(), name=f"runner_{i}"))


if __name__ == "__main__":
    asyncio.run(main())
