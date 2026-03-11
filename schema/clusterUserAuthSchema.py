from pydantic import BaseModel, Field
from typing import Optional

from schema.commonSchema import ROLE

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
    role: ROLE

#------------------------------------ ClusterUserData ----------------------------------------

class ClusterUserData(BaseModel):
    id: str = Field(alias="_id")
    cluster_id: str
    email_id: str
    fullname: str
    username: str
    