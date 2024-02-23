import os
import random
from fastapi.testclient import TestClient
import pytest

# TODO 从零创建数据库并测试

os.environ["account_server_mysql_dsn"] = "mysql+pymysql://tts:askdjflwe234kjkjlr2332f@192.168.196.86:3306/test_tts"

from ..app import appserver

client = TestClient(appserver)


class TestApiAccount():



    @pytest.mark.parametrize("password,except_status", [
        ("ABCdsf@123", 200),
        ("123", 422),
        ('abc123', 422),
        ('ABCdsf123', 422)
    ])
    def test_add_account_200(self, password, except_status):
        """ 测试
        """

        email = f"test_{random.randrange(1, 99999)}_{
            random.choice('abcdefghijk')}@test.test"
        account_name = f"{random.choice(['asdf', 'sdfsde'])}{random.randrange(1, 99999)}"
        response = client.post("/account/register", data={
            "email": email,
            "account_name": account_name,
            "password": password
        })
        assert response.status_code == except_status
