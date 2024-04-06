
from urllib import parse

import pytest
from src.workers import send_email_worker


class TestClassSendEmailWorker():

    @pytest.fixture(scope="session")
    def config(self):
        return send_email_worker.WorkerConfig()

    def test_smtp_server(self, config):
        smtp_server = send_email_worker.SmtpServer(
            url=config.smtp_server_url.host or "",
            port=config.smtp_server_url.port or 0,
            user=parse.unquote(config.smtp_server_url.username or ""),
            password=parse.unquote(
                config.smtp_server_url.password or ""),
            from_mail=config.smtp_from_mail
        )
        send_ok = smtp_server.send_email(
            to_email="realisvalue@gmail.com",
            subject="account-server unit test",
            body="account-server unit test http://www.google.com"
        )
        assert send_ok, "邮件发送失败"
