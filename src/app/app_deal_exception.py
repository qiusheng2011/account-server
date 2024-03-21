import logging

import sqlalchemy.exc
from fastapi import (
    requests,
    responses
)

from app.application import appserver


logger = logging.getLogger(__name__)


@appserver.exception_handler(sqlalchemy.exc.DatabaseError)
async def deal_db_database_error(request: requests.Request, exc: sqlalchemy.exc.DatabaseError):
    error_msg = f"数据库错误\t{request.url._url}\tsqlalchemy.errorcode={
        exc.code}\t{" ".join(exc.args)}"
    logger.critical(error_msg)
    return responses.PlainTextResponse("server error", status_code=500)


@appserver.exception_handler(RuntimeError)
async def deal_runtime_error(request: requests.Request, exc: RuntimeError):
    error_msg = f"运行错误\t{request.url._url}\t{" ".join(exc.args)}"
    logger.critical(error_msg)
    return responses.PlainTextResponse("server error", status_code=500)
