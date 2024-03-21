# 微服务：account-server（账户中心）

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

    pytest ./tests

### 性能测试

    python -m locust  -H http://127.0.0.1:8700 -f ./tests/apiperformance_test/locustfile.py --headless -u 10 -r 200 -t 1m

## 部署

### 容器部署

    参见 dockerfile
