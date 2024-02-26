# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}

# 设置检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl  ${host}:${port}/health" ]

# 安装测试框架
RUN  pip install  locust  pytest

# 安装依赖
COPY   ./requirements.txt /appserver/
RUN pip install --no-cache-dir  --upgrade  -r /appserver/requirements.txt

COPY ./src/   /appserver/src/
WORKDIR /appserver/src
CMD ["python", "./main.py"]
