
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends

from schema.clusterAdminAuthSchema import APIResponse, LoginCredentials
from service.MeeQ_service.Cluster_AdminAuthService import ClusterAdminAuthService


cluster_admin_auth_resourse = APIRouter()


@cbv(cluster_admin_auth_resourse)
class ClusterAdminAuthResourse:

    def __init__(self,clusterAdminAuthService:ClusterAdminAuthService= Depends()):
        self.clusterAdminAuthService=clusterAdminAuthService
    
    @cluster_admin_auth_resourse.post("/ClusterAdminLogin",response_model=APIResponse)
    def cluster_login(self,login_credentials: LoginCredentials):
        return self.clusterAdminAuthService.login_cluster_admin(login_credentials)