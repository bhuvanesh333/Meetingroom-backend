import datetime
from typing import Optional
from pydantic import BaseModel

class TimeSlot(BaseModel):
    id: int
    username: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    description: Optional[str] = None