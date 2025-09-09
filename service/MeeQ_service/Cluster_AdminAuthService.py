



from fastapi import Depends
from repository.MeeQ_repository.Cluster_AdminRepository import ClusterAdminRepository
from schema.clusterAdminAuthSchema import APIResponse, LoginCredentials


class ClusterAdminAuthService:
    
    def __init__(self,clusterAdminRepository:ClusterAdminRepository=Depends()):
        self.clusterAdminRepository=clusterAdminRepository

    def login_cluster_admin(self,login_credentials:LoginCredentials)->APIResponse:
        creds_dict = {
            "Cluster_ID":login_credentials.clusterId,
            "Cluster_Password":login_credentials.password
        }
        result = self.clusterAdminRepository._get_cluster_admin_by_fiels(creds_dict)
        print(result)
        return APIResponse(
            message="Login successful" if result else "Login failed",
            error="" if result else "Invalid credentials"
        )