from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class ClusterLoginRequest(BaseModel):
    cluster_id: str
    password: str