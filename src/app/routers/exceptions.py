import logging
from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status

logger = logging.getLogger()


class PasswordIllegalHTTPException(HTTPException):
    """ 密码问题
    """

    def __init__(self, *args: object) -> None:
        super().__init__(status_code=422, detail="密码不合规")


class AuthenticateUserFailed(HTTPException):
    """ 验证失败
    """

    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Incorrect username or password",
                         headers={"WWW-Authenticate": "Bearer"})


class AuthenticateFailed(HTTPException):
    """ 验证失败
    """

    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Incorrect Certificate",
                         headers={"WWW-Authenticate": "Bearer"})


class AuthenricateRefreshTokenError(HTTPException):
    """ refresh token 无效错误
    """

    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST,
                         "The provided authorization grant or refresh token is invalid, expired or revoked")
