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
                "cluster_id": login_credential.cluster_id,
                "password": login_credential.password
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
                data = login_credential.cluster_id
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
                "cluster_id": signup_credential.cluster_id
            })
            if existing_cluster:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cluster ID already exists"
                )
            
            existing_email = self.clusterAdminRepository._get_cluster_admin_by_fields({
                "email_id": signup_credential.email_id
            })
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email ID already exists"
                )

            creds_dict = {
                "cluster_id": signup_credential.cluster_id,
                "password": signup_credential.password,
                "admin_name": signup_credential.admin_name,
                "email_id": signup_credential.email_id,
                "organization_name": signup_credential.organization_name
            }
            
            result = self.clusterAdminRepository._set_cluster_admin_by_fields(creds_dict)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create cluster admin"
                )
            
            creds_dict = {
                "cluster_id": signup_credential.cluster_id,
                "buildings":[]
            }

            result=self.clusterAdminRepository.create_conference_room(creds_dict)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create clustermeetingroom"
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
                "cluster_id": clusterid
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
