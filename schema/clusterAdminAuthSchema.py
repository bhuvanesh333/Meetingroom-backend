from pydantic import BaseModel
from typing import Any, Optional

class LoginCredential(BaseModel):
    cluster_id: str
    password: str

# ---------------------------------- SignUp ------------------------------------

class SignupCredential(BaseModel):
    admin_name: str
    email_id: str
    organization_name: str
    cluster_id: str
    password: str
    
class ClusterIdCheckRequest(BaseModel):
    cluster_id: str