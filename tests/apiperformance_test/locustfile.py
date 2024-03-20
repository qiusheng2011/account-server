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
    def get_token(self):
        signin_response = self.client.post("/account/v2/authorization", data={
            "password": "abcABC@123",
            "username": "test@test.com",
            "grant_type": "password"
        })
        if signin_response.status_code == 200:
            data = signin_response.json()
            access_token = data.get("access_token")
            if access_token:
                self.client.get("/account/me", headers={
                    "Authorization": "bearer " + access_token
                })
