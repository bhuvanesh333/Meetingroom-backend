
from fastapi import Depends,status
from fastapi.responses import JSONResponse


from repository.ClusterRoom.ClusterRoomAuthRepository import ClusterRoomAuthRepository
from utils.auth_utils import hash_password


class ClusterAuthResourceService:
    def __init__(self,clusterroomauthRepository:ClusterRoomAuthRepository=Depends()):
        self.repository = clusterroomauthRepository

    def cluster_authCheck(self,cluster_id,password):
        
        user= self.repository._get_clusterroom_cluster_user_field({"Cluster_ID": cluster_id})
        if not user:
            return JSONResponse(
                content={"message": "Invalid cluster_id or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # hashed_input = hash_password(password)
        hashed_input = password
        if user.get("Cluster_Password") != hashed_input:
            return JSONResponse(
                content={"message": "Invalid cluster_id or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return JSONResponse(
            content={"message": "Login successful", "_id": str(user["_id"]),"cluster_id":str(user["Cluster_ID"])},
            status_code=status.HTTP_200_OK
        )