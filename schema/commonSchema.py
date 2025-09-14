from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    message: str
    error: str
    data: Optional[Any] = None