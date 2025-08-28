
from fastapi import Depends, HTTPException,status


from repository.MeetingRoom.MeetingRoomRepository import MeetingRoomRepository

class ClusterRoomService:
    def __init__(self,meetingRoomRepository:MeetingRoomRepository=Depends()):
        self.repository = meetingRoomRepository

    