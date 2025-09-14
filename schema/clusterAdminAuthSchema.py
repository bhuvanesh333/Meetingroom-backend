from pydantic import BaseModel
from typing import Any, Optional

class LoginCredential(BaseModel):
    clusterId:str
    password:str

# ---------------------------------- SignUp ------------------------------------

class SignupCredential(BaseModel):
    adminName:str
    emailId:str
    organizationName:str
    clusterId:str
    password:str
    
class ClusterIdCheckRequest(BaseModel):
    clusterId: str    
    