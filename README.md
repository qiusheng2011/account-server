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

### 依赖

- python: >3.12

- python-sitepackages: 查看 [requirements.txt](./requirements.txt)

### 配置项

```
  环境变量名 要全小写 要么全大写，否则不生效。 
```

#### server
##### 环境变量字段（前缀 account_server_{field}）
| field | type | default | name  | explain |
| :---- | :--- | :------ | :------ | :------ |
| server_name| str | account_server | 服务名 | - |
| host | str | 127.0.0.1 | 启动地址 | |
| port | int | 8700 | 启动端口 | |
| debug | bool | False | 调试开关 | |
| workers| int | 1 | 服务启动进程数| |
| access_token_expire_minutes| int | 60 | 凭证失效时间（分钟）| |
| refresh_token_expire_extra_minutes| int| 1440 | 刷新凭证失效（1440分钟=默认1天）| |
| token_secret_key | str | xxxxxx | 凭证加密密钥 | |
| token_algorithm | str | HS256 | 凭证加密算法 | |
| log_dir | str | server_dir/../ | 日志路径 | |
| log_prefix | str | account_server | 日志前缀 |
| mysql_dsn | str | None | mysql数据库地址 | |
| mysql_connect_args | dict | { "connect_timeout": 3 } | |
| redis_dsn | str | None | redis地址 | |

#### worker

##### SendEmailWorker 环境变量字段（前缀 account_server_worker_{field}）
| field | type | default | name  | explain |
| :---- | :--- | :------ | :------ | :------ |
| redis_dsn | str | None | redis地址 | |
| smtp_servser_url | str | None | SMTP服务地址 | |
| smtp_servser_user | str | None | SMTP服务用户名 | |
| smtp_server_password | str | None| SMTP服务用户密码| |
| account_activate_weburl_f | str | None | 账户激活的web地址格式化字符串| |

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

    # worker 启动
    python ./src/workers/send_email_workers.py
```
