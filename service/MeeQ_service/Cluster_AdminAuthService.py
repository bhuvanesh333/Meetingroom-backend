from fastapi import Depends, HTTPException, status
from repository.MeeQ_repository.Cluster_AdminRepository import ClusterAdminRepository
from repository.MeeQ_repository.Cluster_UserSessionsRepository import ClusterUserSessionsRepository
from schema.clusterAdminAuthSchema import LoginCredential, SignupCredential
from schema.commonSchema import APIResponse
from auth.jwt_token_manger import token_manager_singleton

class ClusterAdminAuthService:
    
    def __init__(self, clusterAdminRepository: ClusterAdminRepository = Depends(),
                clusterUserSessionsRepository:ClusterUserSessionsRepository = Depends()):
        self.clusterAdminRepository = clusterAdminRepository
        self.clusterUserSessionsRepository = clusterUserSessionsRepository

    def set_active_status(self,user_id:str,is_online:bool):
        result = self.clusterAdminRepository._set_active_status(user_id,is_online)
        if result>0:
            return True
        raise HTTPException(
                    status_code=status.HTTP_304_NOT_MODIFIED,
                    detail="Not Modified"
                )
    def session_token_action(self,user_id,session_token:str):
        #check user_id is available? 2. check is active bit
        session_token_hased = token_manager_singleton.hash_token(session_token)
        if self.clusterUserSessionsRepository._is_session_empty():
            session_id = self.clusterUserSessionsRepository._create_user_session(user_id, session_token_hased)
            return
   
        session_resp = self.clusterUserSessionsRepository._get_user_session(user_id)
        if session_resp is None:
            session_id = self.clusterUserSessionsRepository._create_user_session(user_id, session_token_hased)
            return

        if session_resp is not None:
            self.clusterUserSessionsRepository._update_user_session(user_id,session_token_hased,True)


    def login_cluster_admin(self, login_credential: LoginCredential) -> APIResponse:
        try:
            cred_dict={}
            if login_credential.cluster_id != "":
                creds_dict = {
                    "cluster_id": login_credential.cluster_id,
                    "password": login_credential.password
                }
            elif login_credential.email_id != "":
                cred_dict = {
                    "email_id": login_credential.email_id,
                    "password": login_credential.password
                }

            result = self.clusterAdminRepository._get_cluster_admin_by_fields(creds_dict)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            set_active_status = self.set_active_status(str(result["_id"]), True)

            session_token = token_manager_singleton.generate_session_token()
            self.session_token_action(str(result["_id"]),session_token)
            access_token = token_manager_singleton.create_access_token(data={"sub": str(result["_id"]), "role": "cluster_admin", "session_token": session_token})
            refresh_token = token_manager_singleton.create_refresh_token(data={"sub": str(result["_id"]), "role": "cluster_admin"})
            
            response = {
                "_id":str(result["_id"]),
                "cluster_id":result["cluster_id"],
                "email_id":result["email_id"],
                "admin_name":result["admin_name"],
                "organization_name":result["organization_name"],
                "token":access_token,
                "refresh_token":refresh_token
            }
            
            return APIResponse(
                message="Login successful",
                error="",
                data = response
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
                "organization_name": signup_credential.organization_name,
                "role": signup_credential.role,
                "is_online": False
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
