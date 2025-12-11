from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    message: str
    error: str
    data: Optional[Any] = None

class user_Session(BaseModel):
    user_id: str
    session_token: str
    is_active: bool
    expire_at: datetime
    last_accessed: datetime