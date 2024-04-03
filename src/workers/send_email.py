import datetime
from typing import Optional
import smtplib
from email.mime import text as email_text
from email.mime import multipart as email_multipart

from redis import asyncio as asyncio_redis
import pydantic



class Event(pydantic.BaseModel):

    event_name: str
    event_time: datetime.datetime
    data: Optional[dict]


class SmtpServer(pydantic.BaseModel):

    smtp_url: str = "smtp.mail.me.com"
    smtp_port: int = 587

    smtp_server_user: str = ""
    smtp_server_password: str = ""
    smtp_from_mail: str = "schoupdev@icloud.com"

    def send_email(self, to_email, subject, body):
        message = email_multipart.MIMEMultipart()
        message["from"] = self.smtp_from_mail
        message["to"] = to_email
        message["Subject"] = subject
        message.attach(email_text.MIMEText(body))

        with smtplib.SMTP(host=self.smtp_url, port=self.smtp_port) as server:
            server.starttls()
            server.login(
                user=self.smtp_server_user,
                password=self.smtp_server_password
            )

            server.send_message(message)
            print(f"to-email:{to_email}>发送成功")


class EmailSendWorker():

    channel_name = "account-server"

    def __init__(self, event_db_pool, smtp_server):
        self.event_db_pool = event_db_pool
        self.smtp_server = smtp_server

    def send_account_activate_email(self, register_success_event):
        pass

    async def run(self):
        while True:
            async with asyncio_redis.Redis.from_pool(self.event_db_pool) as async_redis:
                event_str = await async_redis.rpop(self.channel_name)

                event = Event.model_validate_json(
                    event_str) if event_str else None


if __name__ == "__main__":
    SmtpServer().send_email("realisvalue@gmail.com", "test", "test")
