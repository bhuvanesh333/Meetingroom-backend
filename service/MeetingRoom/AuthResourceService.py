
from fastapi import Depends,status
from fastapi.responses import JSONResponse


from repository.MeetingRoom.MettingRoomAuthRepository import MeetingRoomAuthRepository
from utils.auth_utils import hash_password


class AuthResourceService:
    def __init__(self,meetingroomauthRepository:MeetingRoomAuthRepository=Depends()):
        self.repository = meetingroomauthRepository

    def authCheck(self,username,password):
        
        user= self.repository._get_meetingroom_user_field({"username": username})

        if not user:
            return JSONResponse(
                content={"message": "Invalid username or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # hashed_input = hash_password(password)
        hashed_input = password
        if user.get("password") != hashed_input:
            return JSONResponse(
                content={"message": "Invalid username or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return JSONResponse(
            content={"message": "Login successful", "user_id": str(user["_id"]),
                     "name": str(user["name"]),"username":str(user["username"]),"Cluster_ID":str(user["Cluster_ID"])},
            status_code=status.HTTP_200_OK
        )
    
    def cluster_authCheck(self,cluster_id,password):
        
        user= self.repository._get_meetingroom_cluster_user_field({"Cluster_ID": cluster_id})

        if not user:
            return JSONResponse(
                content={"message": "Invalid cluster_id or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # hashed_input = hash_password(password)
        hashed_input = password
        if user.get("password") != hashed_input:
            return JSONResponse(
                content={"message": "Invalid cluster_id or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return JSONResponse(
            content={"message": "Login successful", "cluster_id": str(user["_id"])},
            status_code=status.HTTP_200_OK
        )