""" API测试-pytest脚本

当前测试范围：
    注册，登陆，个人信息
"""

import time
import random
import pytest
from httpx import AsyncClient


from src.app import appserver


# TODO 从零创建数据库并测试


class TestApiAccount():

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def async_client(self):
        async with AsyncClient(app=appserver, base_url="http://localhost") as client:
            yield client

    @pytest.mark.parametrize("password,except_status", [
        ("ABCdsf@123", 200),
        ("123", 422),
        ("abc123", 422),
        ("ABCdsf123", 422)
    ])
    @pytest.mark.asyncio
    async def test_1_account_200(self, password, except_status,  async_client: AsyncClient):
        """ 测试
        """
        # async with AsyncClient(app=appserver, base_url="http://localhost") as client:
        client = async_client
        timestamp_s = int(time.time()*100000)
        email = f"test_{timestamp_s}_{random.randrange(1, 99999)}_{
            random.choice('abcdefghijk')}@test.test"
        account_name = f"{random.choice(['asdf', 'sdfsde'])}{
            random.randrange(1, 99999)}"
        post_data = {
            "email": email,
            "account_name": account_name,
            "password": password
        }
        register_response = await client.post("/account/register", data=post_data)
        assert register_response.status_code == except_status, f"{
            str(post_data)}"
        if register_response.status_code == 200:
            pass
        else:
            return False, None, None
        signin_responce = await client.post("/account/v2/authorization", data={
            "username": email,
            "password": password,
            "grant_type": "password"
        })
        assert signin_responce.status_code == 200
        data = signin_responce.json()
        assert "access_token" in data
        assert data.get("token_type") == "bearer"

        me_response = await client.get("/account/me", headers={
            "Authorization": "bearer " + data["access_token"]
        })
        assert me_response.status_code == 200
        account_info = me_response.json()
        assert account_info.get("account_name", None) == account_name
        aid = account_info.get("aid", None)

        delete_response = await client.delete("/account/me", headers={
            "Authorization": "bearer " + data["access_token"]
        })
        assert me_response.status_code == 200
        account_info = delete_response.json()
        assert account_info["rst"].get("aid", None) == aid
