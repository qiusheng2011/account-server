import sys
import os
import datetime
import logging
from typing import Optional
import smtplib
from email.mime import text as email_text
from email.mime import multipart as email_multipart

from redis import asyncio as asyncio_redis
import pydantic

logger = logging.getLogger(__name__)

SMTP_SERVER_USER_KEY = "account_server_worker_smtp_server_user"
SMTP_SERVER_USER = os.getenv(SMTP_SERVER_USER_KEY) or os.getenv(
    SMTP_SERVER_USER_KEY.upper())
SMTP_SERVER_PASSWORD_KEY = "account_server_worker_smtp_server_password"
SMTP_SERVER_PASSWORD = os.getenv(SMTP_SERVER_PASSWORD_KEY) or os.getenv(
    SMTP_SERVER_PASSWORD_KEY.upper())

if not SMTP_SERVER_USER or not SMTP_SERVER_PASSWORD:
    raise ValueError(f"无法获取到环境变量 {SMTP_SERVER_USER_KEY} or {
                     SMTP_SERVER_PASSWORD} ")


class Event(pydantic.BaseModel):

    event_name: str
    event_time: datetime.datetime
    data: Optional[dict] = pydantic.Field(default_factory=dict)


class SmtpServer(pydantic.BaseModel):

    url: str = "smtp.mail.me.com"
    port: int = 587

    user: Optional[str]
    password: Optional[str]
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
                print(f"to-email:{to_email}>发送成功")
                return True
        except smtplib.SMTPAuthenticationError as ex:
            logging.critical(str(ex))
            return False


class EmailSendWorker():

    channel_name = "account-server"

    def __init__(self, event_db_pool, smtp_server):
        self.event_db_pool = event_db_pool
        self.smtp_server = smtp_server

    def make_account_activate_body(self, email, aid):
        pass 

    def send_account_activate_email(self, register_success_event):
        account_email = register_success_event.data.get("email", None)
        account_aid = register_success_event.data.get("aid", None)
        if not account_email or account_aid:
            logger.error(f"event:{register_success_event.name}.data 无法获取 email 或者 aid")
            return False
        

    async def run(self):
        while True:
            async with asyncio_redis.Redis.from_pool(self.event_db_pool) as async_redis:
                event_str = await async_redis.rpop(self.channel_name)

                event = Event.model_validate_json(
                    event_str) if event_str else None
                self.send_account_activate_email(event)

if __name__ == "__main__":
    # SmtpServer().send_email("", "test", "test")
    pass
