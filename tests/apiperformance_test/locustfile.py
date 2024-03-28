"""API性能测试-locust脚本

"""
import time
import random
from locust import HttpUser, task


def get_account_name_and_email():
    account_name = f"locusttest_{int(time.time()*1000000)}_{
        random.randrange(0, 100)}"
    email = f"{account_name}@locusttest.com"

    return account_name, email


class PTestUser(HttpUser):

    @task
    def ptest_health(self):
        self.client.get("/health")


class PtestAccountSignIn(HttpUser):

    account_name: str = ""
    email: str = ""

    def on_start(self):
        self.account_name, self.email = get_account_name_and_email()
        response = self.client.post("/account/register", data=dict(
            email=self.email,
            account_name=self.account_name,
            password="abcABC@123"
        ))
        if response.status_code != 200:
            self.stop(force=True)
            raise ValueError("注册失败")

    def on_stop(self):
        signin_response = self.client.post("/account/v2/authorization", data={
            "password": "abcABC@123",
            "username": self.email,
            "grant_type": "password"
        })
        if signin_response.status_code == 200:
            data = signin_response.json()
            access_token = data.get("access_token")
            self.client.delete("/account/me",
                               headers={
                                   "Authorization": "bearer " + access_token
                               })

    @task
    def test_get_token(self):
        """登陆并访问个人信息
        """
        signin_response = self.client.post("/account/v2/authorization", data={
            "password": "abcABC@123",
            "username": self.email,
            "grant_type": "password"
        })
        if signin_response.status_code == 200:
            data = signin_response.json()
            access_token = data.get("access_token")
            if access_token:
                self.client.get("/account/me",
                                headers={
                                    "Authorization": "bearer " + access_token
                                })
                self.access_token = access_token
