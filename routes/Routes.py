from fastapi import FastAPI

from routes.MeetingRoom.AuthResouces import auth_resourse
from routes.ClusterRoom.ClusterAuthResource import cluster_auth_resourse
from routes.MeetingRoom.MeetingRoomResource import meetingroom_resourse


class IncludeRoutes:

    def __init__(self,app:FastAPI) :
        self.app = app
        self.includeRoutes()
    
    def includeRoutes(self):
        self.app.include_router(auth_resourse, prefix="/api/MeetingRoom_auth", tags=["MeetingRoom_auth"])
        self.app.include_router(cluster_auth_resourse, prefix="/api/ClusterRoom_auth", tags=["ClusterRoom_auth"])
        self.app.include_router(meetingroom_resourse, prefix="/api/MeetingRoom", tags=["MeetingRoom"])
