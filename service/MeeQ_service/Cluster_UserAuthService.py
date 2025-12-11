
from bson import ObjectId
from fastapi import Depends
from datetime import datetime, timezone
from auth.jwt_token_manger import token_manager_singleton
from repository.MeeQ_repository.Cluster_AdminRepository import ClusterAdminRepository
from repository.MeeQ_repository.Cluster_UserRepository import ClusterUserRepository
from repository.MeeQ_repository.Cluster_UserSessionsRepository import ClusterUserSessionsRepository
from schema.clusterUserAuthSchema import ClusterUserData, UserLoginCredential, UserSignupCredential
from schema.commonSchema import APIResponse
from fastapi import HTTPException, status


class ClusterUserAuthService:

    def __init__(self,clusterUserRepository:ClusterUserRepository = Depends(),
                 clusterAdminRepository: ClusterAdminRepository = Depends(),
                 clusterUserSessionsRepository:ClusterUserSessionsRepository = Depends(),):
        self.clusterUserRepository = clusterUserRepository
        self.clusterAdminRepository = clusterAdminRepository
        self.clusterUserSessionsRepository = clusterUserSessionsRepository

    def set_active_status(self,user_id:str,is_active:bool):
        result = self.clusterUserRepository._set_active_status(user_id,is_active)
        if result>0:
            return APIResponse(message="Active status updated successfully", error="", data=result)
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

    def login_cluster_user(self,userLoginCredential:UserLoginCredential) -> APIResponse:
        try:
            cred_dict={}
            if userLoginCredential.username != "":
                cred_dict = {
                    "username": userLoginCredential.username,
                    "password": userLoginCredential.password
                }
            elif userLoginCredential.email_id != "":
                cred_dict = {
                    "email_id": userLoginCredential.email_id,
                    "password": userLoginCredential.password
                }
                
            result = self.clusterUserRepository._get_cluster_user_by_fields(cred_dict)
        
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username/email or password."
                )
            
            set_active_status = self.set_active_status(str(result["_id"]), True)
            
            if not result["approval"]:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Approval Not Granted By Cluster Admin"
                )

            if "_id" in result and isinstance(result["_id"], ObjectId):
                result["_id"] = str(result["_id"])
            
            session_token = token_manager_singleton.generate_session_token()
            self.session_token_action(result["_id"],session_token)
            access_token = token_manager_singleton.create_access_token(data={"sub": result["_id"], "role": "cluster_user", "session_token": session_token})
            refresh_token = token_manager_singleton.create_refresh_token(data={"sub": result["_id"], "role": "cluster_user"})
            response = {
                "_id":result["_id"],
                "cluster_id":result["cluster_id"],
                "email_id":result["email_id"],
                "fullname":result["fullname"],
                "username":result["username"],
                "token":access_token,
                "refresh_token":refresh_token
            }

            return APIResponse(message="Cluster Login success", error="", data=response)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

    def signup_cluster_user(self, userSignupCredential: UserSignupCredential) -> APIResponse:
        try:
            cred_dict = {"cluster_id": userSignupCredential.cluster_id}
            result = self.clusterAdminRepository._get_cluster_admin_by_fields(cred_dict)
            
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cluster_ID Not Found"
                )
        
            cred_dict = {"username": userSignupCredential.username}
            result = self.clusterUserRepository._get_cluster_user_by_fields(cred_dict)
            
            if result is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists"
                )
            
            cred_dict = {"email_id": userSignupCredential.email_id}
            result = self.clusterUserRepository._get_cluster_user_by_fields(cred_dict)
            
            if result is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email ID already exists"
                )
            
            cred_dict = {"cluster_id": userSignupCredential.cluster_id,
                         "email_id":userSignupCredential.email_id,
                         "password":userSignupCredential.password,
                         "username":userSignupCredential.username,
                         "fullname":userSignupCredential.fullname,
                         "approval":False,
                         "approval_req_time":datetime.now(timezone.utc),
                         "approval_grant_time":datetime.now(timezone.utc),
                         "last_active":datetime.now(timezone.utc),
                         }
            
            result = self.clusterUserRepository._set_cluster_user_by_fields(cred_dict)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create clusteruser"
                )
            return APIResponse(message="clusteruser create success", error="")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

    def logout_cluster_user(self,cluster_user_data:ClusterUserData) -> APIResponse:
        try:
       
            res=self.clusterUserRepository._set_active_status(cluster_user_data.id,False)
            res=self.clusterUserSessionsRepository._update_user_session(cluster_user_data.id,"",False)
            return APIResponse(message="Cluster Logout success", error="", data="")

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
