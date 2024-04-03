import datetime
from typing import Optional
import pydantic


class RegisterSuccessEvent(pydantic.BaseModel):

    event_name: str = "RegisterSuccessEvent"
    event_time: datetime.datetime =  pydantic.Field(default_factory=datetime.datetime.now)
    data: Optional[dict] = None
