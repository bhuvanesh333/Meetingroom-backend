
from datetime import datetime, timezone
import random
import time
from fastapi import Depends, HTTPException, status
from repository.MeeQ_repository.Cluster_UserPageRepository import ClusterUserPageRepository
from schema.clusterUserPageSchema import TimeSlot
from schema.commonSchema import APIResponse


class ClusterUserPageService:
    def __init__(self,clusterUserPageRepository:ClusterUserPageRepository= Depends()):
        self.clusterUserPageRepository=clusterUserPageRepository

    def get_all_booking_list(self,Cluster_ID:str)-> APIResponse:
        result = self.clusterUserPageRepository._get_all_booking_list(Cluster_ID)
        if not result:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to Fetch Building"
                )
        return APIResponse(message="fetching success", error="",data=result)

    def gen_random_id(self, Cluster_ID: str, Building_ID: str) -> int:
        cluster = self.clusterUserPageRepository._get_all_timeslot_id(Cluster_ID,Building_ID)
        ids = [b["id"] for b in cluster.get("timeSlots", []) if "id" in b]
        while True:
            new_id = random.randint(1000, 9999)
            if new_id not in ids:
                return new_id

    def validate_time_slot(self, timeSlot: TimeSlot):
        now = datetime.now()
        fake_utc_now = now.replace(tzinfo=timezone.utc)
        if(fake_utc_now.timestamp()-60 > timeSlot.start_time.timestamp() or fake_utc_now.timestamp()-60 > timeSlot.end_time.timestamp()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Time Slot: start_time and end_time must be in the future"
            )
        
        if timeSlot.start_time >= timeSlot.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Time Slot: start_time must be before end_time"
            )     
        
    def add_time_slot(self, timeSlot: TimeSlot, Cluster_ID: str, Building_ID: str) -> APIResponse:
        self.validate_time_slot(timeSlot)
        timeSlot.id = self.gen_random_id(Cluster_ID,Building_ID)
        result = self.clusterUserPageRepository._add_time_slot(timeSlot, Cluster_ID, Building_ID)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to Add Time Slot"
            )
        return APIResponse(message="Time Slot added successfully", error="", data=result)

    def stream_conference_room_to(self, Cluster_ID: str, room_id: str):
        try:
            result = self.clusterUserPageRepository._get_conferenceroom_booking(Cluster_ID, room_id)
    
            if not result:
                return {
                    "status": "error",
                    "message": "Failed to Fetch Building",
                    "timestamp": time.strftime('%H:%M:%S')
                }
            
            return {
                "status": "success",
                "data": result["buildings"],
                "timestamp": time.strftime('%H:%M:%S')
            }
            
        except Exception as e:
            print(f"Error in stream_conference_room_to: {str(e)}")
            return {
                "status": "error",
                "message": f"Internal server error: {str(e)}",
                "timestamp": time.strftime('%H:%M:%S')
            }
    def delete_time_slot(self, TimeSlot_ID: int, Cluster_ID: str) -> APIResponse:
        result = self.clusterUserPageRepository.delete_time_slot(Cluster_ID, TimeSlot_ID)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to Delete Time Slot"
            )
        return APIResponse(message="Time Slot deleted successfully", error="", data=result.modified_count)