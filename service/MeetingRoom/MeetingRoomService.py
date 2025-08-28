
from fastapi import Depends, HTTPException,status


from repository.MeetingRoom.MeetingRoomRepository import MeetingRoomRepository



class MeetingRoomService:
    def __init__(self,meetingRoomRepository:MeetingRoomRepository=Depends()):
        self.repository = meetingRoomRepository

    def getBuldingByClusterId(self,cluster_id:str):
        document= self.repository.get_buildings(cluster_id)
        if not document:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return document["Buildings"]
    
    def getTimeSlotByClusterID_ID(self,cluster_id:str,building_id=int):
        document = self.repository.get_timeslots(cluster_id)
        if not document:
            raise HTTPException(status_code=404, detail="Cluster not found")
        
        building = next((b for b in document.get("Buildings", []) if str(b.get("id")) == str(building_id)), None)

        if not building:
            raise HTTPException(status_code=404, detail="Building not found")


        return {"timeSlots": building.get("timeSlots", [])}
   