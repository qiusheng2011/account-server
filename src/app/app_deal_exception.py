import logging

from sqlalchemy.exc import (
    DatabaseError
)
from fastapi.responses import (
    PlainTextResponse
)
from fastapi.requests import Request

from .app import appserver

logger = logging.getLogger(__name__)


@appserver.exception_handler(DatabaseError)
async def deal_db_database_error(request: Request, exc: Exception):
    error_msg = f"数据库错误\t{request.url._url}\tsqlalchemy.errorcode={
        exc.code}\t{' '.join(exc.args)}"
    logger.error(error_msg)
    return PlainTextResponse("server error", status_code=500)
