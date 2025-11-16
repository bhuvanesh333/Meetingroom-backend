
from bson import ObjectId
from fastapi import Depends
from datetime import datetime
from repository.MeeQ_repository.Cluster_AdminRepository import ClusterAdminRepository
from repository.MeeQ_repository.Cluster_UserRepository import ClusterUserRepository
from schema.clusterUserAuthSchema import UserLoginCredential, UserSignupCredential
from schema.commonSchema import APIResponse
from fastapi import HTTPException, status

class ClusterUserAuthService:

    def __init__(self,clusterUserRepository:ClusterUserRepository = Depends(),clusterAdminRepository: ClusterAdminRepository = Depends()):
        self.clusterUserRepository = clusterUserRepository
        self.clusterAdminRepository = clusterAdminRepository

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
            
            if not result["approval"]:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Approval Not Granted By Cluster Admin"
                )

            if "_id" in result and isinstance(result["_id"], ObjectId):
                result["_id"] = str(result["_id"])
            
            response = {
                "_id":result["_id"],
                "cluster_id":result["cluster_id"],
                "email_id":result["email_id"],
                "fullname":result["fullname"],
                "username":result["username"],
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
                         "approval_req_time":datetime.now(),
                         "approval_grant_time":"",
                         "last_active":datetime.now(),
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
