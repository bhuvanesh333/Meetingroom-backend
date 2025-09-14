
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends

from schema.clusterAdminAuthSchema import ClusterIdCheckRequest, LoginCredential, SignupCredential
from schema.commonSchema import APIResponse
from service.MeeQ_service.Cluster_AdminAuthService import ClusterAdminAuthService


cluster_admin_auth_resourse = APIRouter()


@cbv(cluster_admin_auth_resourse)
class ClusterAdminAuthResourse:

    def __init__(self,clusterAdminAuthService:ClusterAdminAuthService= Depends()):
        self.clusterAdminAuthService=clusterAdminAuthService
    
    @cluster_admin_auth_resourse.post("/ClusterAdminLogin",response_model=APIResponse)
    def cluster_login(self,login_credential: LoginCredential):
        return self.clusterAdminAuthService.login_cluster_admin(login_credential)
    
    @cluster_admin_auth_resourse.post("/ClusterAdminSignup",response_model=APIResponse)
    def cluster_signup(self,signup_credential: SignupCredential):
        return self.clusterAdminAuthService.signup_cluster_admin(signup_credential)

    @cluster_admin_auth_resourse.post("/ClusterIdCheck",response_model=APIResponse)
    def cluster_id_check(self, request: ClusterIdCheckRequest):
        return self.clusterAdminAuthService.clusterIdCheck(request.clusterId)