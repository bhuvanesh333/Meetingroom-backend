from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Header
from fastapi_utils.cbv import cbv
from service.MeetingRoom.MeetingRoomService import MeetingRoomService

meetingroom_resourse = APIRouter()


@cbv(meetingroom_resourse)
class MeetingRoomResourse:
    def __init__(self, meetingRoomService: MeetingRoomService = Depends()):
        self.meetingRoomService=meetingRoomService

    @meetingroom_resourse.post("/getMeetingRoom")
    def get_meeting_room(self,cluster_id: str = Header(..., alias="X-cluserId")):
        rooms = self.meetingRoomService.getBuldingByClusterId(cluster_id)
        if not rooms:
            raise HTTPException(status_code=404, detail="No meeting rooms found for this clusterID")
        return rooms
    
    
    @meetingroom_resourse.post("/getMeetingRoomTimeSlot")
    def get_meeting_room_for_booking(self,cluster_id: str = Header(..., alias="X-cluserId"),building_id: str = Header(..., alias="X-buildingId")):
        rooms = self.meetingRoomService.getTimeSlotByClusterID_ID(cluster_id,building_id)
        if not rooms:
            raise HTTPException(status_code=404, detail="No meeting rooms found for this clusterID")
        return rooms

       