# 微服务：account-server（账户中心）

## 服务目标

```
提供账户服务，为所有其他的业务提供账户服务，理论上在公司所有业务中应当有且只有一个账户服务(账户业务)。  
```

## 功能

- 注册（oauth2）
  - 邮箱密码注册
- 登陆授权（oauth2）
  - 邮箱密码登陆
- 账户信息

## CI/CD

 ### github action

    参见 .github/workflows/*.yml

 ## 测试

 ### 功能测试

```shell
# 项目根目录执行
pytest ./tests
```

 ### 性能测试

```shell
# 项目根目录执行
python -m locust  -H http://127.0.0.1:8700 -f ./tests/apiperformance_test/locustfile.py --headless -u 10 -r 200 -t 1m  
```

 ## 部署

 ### 部署方式

 #### 容器部署

    参见 dockerfile

 #### 单机部署

```shell
    # python版本 = 3.12
    pip install -r ./requirements.txt
    # 设置环境变量
    ...
    # 服务启动
    python ./src/main.py  
```
