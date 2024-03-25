"""API性能测试-locust脚本

"""

import random
from locust import HttpUser, task


class PTestUser(HttpUser):

    @task
    def ptest_health(self):
        self.client.get("/health")


class PtestAccountRegister(HttpUser):

    @task
    def register_user(self):
        password = "abcABC@123"
        email = (f"test_{random.randrange(1, 99999)}_"
                 f"{random.choice("abcdefghijk")}@test.test")
        account_name = (f"{random.choice(["asdf", "sdfsde"])}"
                        f"{random.randrange(1, 99999)}")
        register_response = self.client.post("/account/register", data=dict(
            email=email,
            account_name=account_name,
            password=password
        ))
        if register_response.status_code != 200:
            return


class PtestAccountSignIn(HttpUser):

    account_name: str = ""
    email: str = ""

    def on_start(self):
        self.account_name = f"test0{random.randrange(0, 99999999)}"
        self.email = f"{self.account_name}@test.com"
        self.client.post("/account/register", data=dict(
            email=self.email,
            account_name=self.account_name,
            password="abcABC@123"
        ))

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
                self.client.get("/account/me", headers={
                    "Authorization": "bearer " + access_token
                })
