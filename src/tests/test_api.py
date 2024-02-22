from ..main import appserver
import os
import random
from fastapi.testclient import TestClient

os.environ["account_server_mysql_dsn"] = "mysql+pymysql://tts:askdjflwe234kjkjlr2332f@192.168.196.86:3306/test_tts"

# TODO 从零创建数据库并测试
client = TestClient(appserver)


def test_add_account():
    email = f"test_{random.randrange(1, 99999)}_{
        random.choice("abcdefghijk")}@test.test"
    response = client.post("/account/register", data={
        "email": email,
        "account_name": f"{random.choice(["asdf", "sdfsde"])}{random.randrange(1, 99999)}",
        "password": "ABCdsf@123"
    })
    print(response.json())
    assert response.status_code == 200
