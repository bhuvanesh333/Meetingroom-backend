from datetime import datetime
from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel

class APIResponse(BaseModel):
    message: str
    error: str
    data: Optional[Any] = None

class user_Session(BaseModel):
    user_id: str
    session_token: str
    is_online: bool
    expire_at: datetime
    last_accessed: datetime

class ROLE(str,Enum):
    CLUSTER_ADMIN = "cluster_admin",
    CLUSTER_USER = "cluster_user",