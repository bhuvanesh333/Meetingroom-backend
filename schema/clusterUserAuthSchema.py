from pydantic import BaseModel
from typing import Any, Optional

# ---------------------------------- Cluster User Login ------------------------------------

class UserLoginCredential(BaseModel):
    username:Optional[str]
    email:Optional[str]
    password:str
    
# ---------------------------------- Cluster User SignUp ------------------------------------

class UserSignupCredential(BaseModel):
    fullname:str
    username:str
    emailId:str
    clusterId:str
    password:str
    