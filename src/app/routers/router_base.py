from typing import Optional
from pydantic import BaseModel

class BaseReponseModel(BaseModel):

    status:int = 0
    message:str = "ok"
    rst:Optional[dict] = {}

