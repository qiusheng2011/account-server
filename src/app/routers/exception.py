from fastapi import HTTPException

class PasswordIllegalHTTPException(HTTPException):

    def __init__(self, *args: object) -> None:
        super().__init__(status_code=422, detail="密码不合规")