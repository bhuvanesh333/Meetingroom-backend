
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends

from schema.clusterUserAuthSchema import ClusterUserData, UserLoginCredential, UserSignupCredential
from schema.commonSchema import APIResponse
from service.MeeQ_service.Cluster_UserAuthService import ClusterUserAuthService


cluster_user_auth_resourse = APIRouter()


@cbv(cluster_user_auth_resourse)
class ClusterUserAuthResourse:

    def __init__(self,clusterUserAuthService:ClusterUserAuthService= Depends()):
        self.clusterUserAuthService=clusterUserAuthService
    
    @cluster_user_auth_resourse.post("/ClusterUserLogin",response_model=APIResponse)
    def cluster_user_login(self,user_login_credential: UserLoginCredential):
        return self.clusterUserAuthService.login_cluster_user(user_login_credential)

    @cluster_user_auth_resourse.post("/ClusterUserSignup",response_model=APIResponse)
    def cluster_user_signup(self,user_signup_credential: UserSignupCredential):
        return self.clusterUserAuthService.signup_cluster_user(user_signup_credential)
    
    @cluster_user_auth_resourse.post("/ClusterUserLogout",response_model=APIResponse)
    def cluster_user_logout(self,cluster_user_data: ClusterUserData):
        return self.clusterUserAuthService.logout_cluster_user(cluster_user_data)