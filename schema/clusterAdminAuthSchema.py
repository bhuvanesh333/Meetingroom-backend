from pydantic import BaseModel
from typing import Any, Optional

from schema.commonSchema import ROLE

class LoginCredential(BaseModel):
    cluster_id: Optional[str]
    email_id:Optional[str]
    password: str

# ---------------------------------- SignUp ------------------------------------

class SignupCredential(BaseModel):
    admin_name: str
    email_id: str
    organization_name: str
    cluster_id: str
    password: str
    role:ROLE
    
class ClusterIdCheckRequest(BaseModel):
    cluster_id: str