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
        email = f"test_{random.randrange(1, 99999)}_{
            random.choice('abcdefghijk')}@test.test"
        account_name = f"{random.choice(['asdf', 'sdfsde'])}{
            random.randrange(1, 99999)}"
        register_response = self.client.post("/account/register", data=dict(
            email=email,
            account_name=account_name,
            password=password
        ))
        if register_response.status_code != 200:
            return


class PtestAccountSignIn(HttpUser):

    def on_start(self):
        self.client.post("/account/register", data=dict(
            email="test@test.com",
            account_name="test",
            password="abcABC@123"
        ))

    @task
    def signin(self):
        signin_response = self.client.post("/account/signin", data={
            "password": "abcABC@123",
            "username": "test@test.com",
            "grant_type": "password"
        })


class PtestAccountSignIn(HttpUser):

    def on_start(self):
        self.client.post("/account/register", data=dict(
            email="PtestAccountSignIn@test.com",
            account_name="test",
            password="abcABC@123"
        ))
        signin_response = self.client.post("/account/signin", data={
            "password": "abcABC@123",
            "username": "PtestAccountSignIn@test.com",
            "grant_type": "password"
        })
        data = signin_response.json()
        self.access_token = data.get("access_token")

    @task
    def account_me(self):
        self.client.get("/account/me", headers={
            "Authorization": "bearer " + self.access_token
        })
