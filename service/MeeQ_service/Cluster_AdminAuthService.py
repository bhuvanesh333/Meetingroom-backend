from fastapi import Depends, HTTPException, status
from repository.MeeQ_repository.Cluster_AdminRepository import ClusterAdminRepository
from schema.clusterAdminAuthSchema import LoginCredential, SignupCredential
from schema.commonSchema import APIResponse


class ClusterAdminAuthService:
    
    def __init__(self, clusterAdminRepository: ClusterAdminRepository = Depends()):
        self.clusterAdminRepository = clusterAdminRepository

    def login_cluster_admin(self, login_credential: LoginCredential) -> APIResponse:
        try:
            creds_dict = {
                "Cluster_ID": login_credential.clusterId,
                "Cluster_Password": login_credential.password
            }
            result = self.clusterAdminRepository._get_cluster_admin_by_fields(creds_dict)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            return APIResponse(
                message="Login successful",
                error="",
                data = login_credential.clusterId
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error during login: {str(e)}"
            )
    
    def signup_cluster_admin(self, signup_credential: SignupCredential) -> APIResponse:
        try:
            existing_cluster = self.clusterAdminRepository._get_cluster_admin_by_fields({
                "Cluster_ID": signup_credential.clusterId
            })
            if existing_cluster:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cluster ID already exists"
                )
            
            existing_email = self.clusterAdminRepository._get_cluster_admin_by_fields({
                "emailID": signup_credential.emailId
            })
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email ID already exists"
                )

            creds_dict = {
                "Cluster_ID": signup_credential.clusterId,
                "Cluster_Password": signup_credential.password,
                "adminName": signup_credential.adminName,
                "emailID": signup_credential.emailId,
                "organizationName": signup_credential.organizationName
            }
            
            result = self.clusterAdminRepository._set_cluster_admin_by_fields(creds_dict)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create cluster admin"
                )
            
            return APIResponse(
                message="Signup successful",
                error=""
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error during signup: {str(e)}"
            )
        
    def clusterIdCheck(self, clusterid: str) -> APIResponse:
        try:
            result = self.clusterAdminRepository._get_cluster_admin_by_fields({
                "Cluster_ID": clusterid
            })
            available = not bool(result)
            return APIResponse(
                message="ClusterIdCheck",
                error="",
                data=available
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error during cluster ID check: {e}"
            )
