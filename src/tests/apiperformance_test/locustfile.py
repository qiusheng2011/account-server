import random
from locust import HttpUser, task


class PTestUser(HttpUser):

    @task
    def ptest_health(self):
        self.client.get("/health")


class PtestAccountRegister(HttpUser):

    @task
    def register_user(self):
        email = f"test_{random.randrange(1, 99999)}_{
            random.choice('abcdefghijk')}@test.test"
        account_name = f"{random.choice(['asdf', 'sdfsde'])}{
            random.randrange(1, 99999)}"
        self.client.post("/account/register", data=dict(
            email=email,
            account_name=account_name,
            password="abcABC@123"
        ))
