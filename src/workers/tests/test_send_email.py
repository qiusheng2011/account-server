
from src.workers import send_email_worker


class TestClassSendEmailWorker():

    def test_smtp_server(self):
        smtp_server = send_email_worker.SmtpServer(
            user=send_email_worker.SMTP_SERVER_USER,
            password=send_email_worker.SMTP_SERVER_PASSWORD
        )
        send_ok = smtp_server.send_email(
            to_email="realisvalue@gmail.com",
            subject="account-server unit test",
            body="account-server unit test http://www.google.com"
        )
        assert send_ok, "邮件发送失败"

