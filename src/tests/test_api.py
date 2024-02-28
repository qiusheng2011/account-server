import os
import random
from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient

# TODO 从零创建数据库并测试


from ..app import appserver


class TestApiAccount():

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def async_client(self):
        async with AsyncClient(app=appserver, base_url="http://localhost") as client:
            yield client

    @pytest.mark.parametrize("password,except_status", [
        ("ABCdsf@123", 200),
        ("123", 422),
        ('abc123', 422),
        ('ABCdsf123', 422)
    ])
    @pytest.mark.asyncio
    async def test_1_add_account_200(self, password, except_status,  async_client: AsyncClient):
        """ 测试
        """
        #async with AsyncClient(app=appserver, base_url="http://localhost") as client:
        client = async_client
        email = f"test_{random.randrange(1, 99999)}_{
            random.choice('abcdefghijk')}@test.test"
        account_name = f"{random.choice(['asdf', 'sdfsde'])}{
            random.randrange(1, 99999)}"
        response = await client.post("/account/register", data={
            "email": email,
            "account_name": account_name,
            "password": password
        })
        assert response.status_code == except_status
        if response.status_code == 200:
            pass
        else:
            return False, None, None
        responce = await client.post("/account/signin", data={
            "username": email,
            "password": password
        })
        assert responce.status_code == 200
        data = responce.json()
        assert "access_token" in data
        assert data.get("token_type") == "bearer"
