from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from schema.MeetingRoom.MeetingRoomAuth import ClusterLoginRequest, LoginRequest
from service.ClusterRoom.ClusterAuthResourceService import ClusterAuthResourceService

cluster_auth_resourse = APIRouter()


@cbv(cluster_auth_resourse)
class ClusterAuthResourse:
    def __init__(self, cluster_authService: ClusterAuthResourceService = Depends()):
        self.cluster_authService=cluster_authService
        
    @cluster_auth_resourse.post("/cluster-login")
    def Cluster_login(self,cluster_payload: ClusterLoginRequest):
        try:
            cluster_id = cluster_payload.cluster_id.strip()
            password = cluster_payload.password.strip()
            return self.cluster_authService.cluster_authCheck(cluster_id,password)
        except HTTPException as e:
                raise e
       

       