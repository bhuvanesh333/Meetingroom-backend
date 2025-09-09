from pydantic import BaseModel
from typing import Any, Optional

class LoginCredentials(BaseModel):
    clusterId:str
    password:str

class APIResponse(BaseModel):
    message: str
    error: str
    data: Optional[Any] = None

