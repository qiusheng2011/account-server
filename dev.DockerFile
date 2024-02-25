# syntax=docker/dockerfile:1
FROM python:3.12

ARG mysql_dsn
ARG host=127.0.0.1
ARG port=8700
ENV account_server_mysql_dsn=$mysql_dsn
ENV account_server_host=$host
ENV account_server_port=$port

# 设置检查

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl  ${host}:${port}/health" ]

COPY   ./requirements.txt /appserver/
RUN pip install --no-cache-dir  --upgrade  -r /appserver/requirements.txt
RUN  pip install  locust  pytest

COPY ./src/   /appserver/src/
WORKDIR /appserver/src

EXPOSE $port/tcp
CMD ["python", "./main.py"] 
