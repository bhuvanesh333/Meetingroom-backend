from pydantic import BaseModel
from typing import Optional

# ---------------------------------- Cluster User Login ------------------------------------

class UserLoginCredential(BaseModel):
    username:Optional[str]
    email_id:Optional[str]
    password:str
    
# ---------------------------------- Cluster User SignUp ------------------------------------

class UserSignupCredential(BaseModel):
    fullname:str
    username:str
    email_id:str
    cluster_id:str
    password:str
    