

import random
from fastapi import Depends, HTTPException, status
from repository.MeeQ_repository.Cluster_PageRepository import ClusterPageRepository
from schema.clusterAdminPageSchema import ConferenceRoom, RoomStatusUpdate
from schema.commonSchema import APIResponse


class ClusterAdminPageService:
    
    def __init__(self,clusterPageRepository:ClusterPageRepository=Depends()):
        self.clusterPageRepository=clusterPageRepository

    def add_cluster_conferenceroom(self, conferenceRoom_data: ConferenceRoom, Cluster_ID: str) -> APIResponse:
        conference_room_dict = {
            "id": self.gen_random_id(Cluster_ID),
            "BuildingName": conferenceRoom_data.BuildingName,
            "Floor": conferenceRoom_data.Floor,
            "ConferenceRoomType": conferenceRoom_data.ConferenceRoomType,
            "ConferenceRoomName": conferenceRoom_data.ConferenceRoomName,
            "Capacity": conferenceRoom_data.Capacity,
            "isAvailable": conferenceRoom_data.isAvailable,
            "imageUrl":conferenceRoom_data.imageUrl
        }

        result = self.clusterPageRepository._set_conference_room_by_fields(conference_room_dict, Cluster_ID)

        # if insert fails → raise HTTPException
        if not result.modified_count:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ConferenceRoom Insert Failed"
            )

        # success → return APIResponse
        return APIResponse(
            message="ConferenceRoom Insert Success",
            error="",
            data={"room_id": conference_room_dict["id"]}
        )

    def gen_random_id(self, Cluster_ID: str) -> int:
        cluster = self.clusterPageRepository._get_all_building_id(Cluster_ID)
        ids = [b["id"] for b in cluster.get("Buildings", []) if "id" in b]
        while True:
            new_id = random.randint(1000, 9999)
            if new_id not in ids:
                return new_id

    def get_cluster_conferenceroom(self, Cluster_ID: str) -> APIResponse:
        buildings = self.clusterPageRepository._get_all_building(Cluster_ID)
        return APIResponse(
            message="ConferenceRoom Fetch Success",
            error="",
            data={"Buildings":buildings["Buildings"]}
        )
    
    def delete_cluster_conferenceroom(self,Room_ID:int,Cluster_ID:str) -> APIResponse:
        self.clusterPageRepository._delete_building_by_Room_Id(Room_ID,Cluster_ID)
        return APIResponse(
            message="ConferenceRoom Delete Success",
            error=""
        )
    
    def update_clusterroom_avail_conferenceroom(self,Room_ID:int,Cluster_ID:str,room_status:RoomStatusUpdate):
        self.clusterPageRepository._update_building_roomstatus(Room_ID,Cluster_ID,room_status.model_dump())
        return APIResponse(
            message="ConferenceRoom status update Success",
            error=""
        )
    
    def update_cluster_conferenceroom(self, conferenceRoom_data: ConferenceRoom, Cluster_ID: str) -> APIResponse:
        conference_room_dict = {
            "id": conferenceRoom_data.id,
            "BuildingName": conferenceRoom_data.BuildingName,
            "Floor": conferenceRoom_data.Floor,
            "ConferenceRoomType": conferenceRoom_data.ConferenceRoomType,
            "ConferenceRoomName": conferenceRoom_data.ConferenceRoomName,
            "Capacity": conferenceRoom_data.Capacity,
            "isAvailable": conferenceRoom_data.isAvailable,
            "imageUrl":conferenceRoom_data.imageUrl
        }

        result = self.clusterPageRepository._update_conference_room_by_fields(conference_room_dict, Cluster_ID)

        if not result.modified_count:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="ConferenceRoom No Changes"
            )

        return APIResponse(
            message="ConferenceRoom Update Success",
            error=""
        )