
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
            
    def add_time_slot(self, timeSlot: TimeSlot, Cluster_ID: str, Building_ID: str) -> APIResponse:
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