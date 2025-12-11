from bson import ObjectId
from database.dataBase_Initializer import ConferenceRoom_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

from schema.clusterUserPageSchema import TimeSlot

class ClusterUserPageRepository:

    def __init__(self):
        self.conferenceRoom_collection = ConferenceRoom_collection

    def _get_all_Conference_room(self):
        try:
            result = self.conferenceRoom_collection.find()
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def delete_time_slot(self,cluster_id:str,timeslot_id:int):
        try:
            result = self.conferenceRoom_collection.update_one(
            { "cluster_id": cluster_id },
            { "$pull": { "buildings.$[].time_slots": { "id": timeslot_id } } }
        )
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _get_all_booking_list(self,Cluster_ID:str):
        try:
            result = self.conferenceRoom_collection.find_one({"cluster_id": Cluster_ID},  
                                        {"buildings": 1, "_id": 0} )
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    def _get_all_timeslot_id(self, Cluster_ID: str, Building_ID: str):
        try:
            cluster = self.conferenceRoom_collection.find_one(
                {"cluster_id": Cluster_ID, "buildings.id": int(Building_ID)},
                {"buildings.$": 1}
            )
            if not cluster:
                raise HTTPException(status_code=404, detail="Cluster or Building not found")
            return cluster["buildings"][0]  # Return the specific building document
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _add_time_slot(self, timeSlot: TimeSlot, Cluster_ID: str, Building_ID: str):
        try:
            result = self.conferenceRoom_collection.update_one(
                {"cluster_id": Cluster_ID, "buildings.id": int(Building_ID)},
                {"$push": {"buildings.$.time_slots": timeSlot.model_dump()}}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Building not found or Time Slot not added")
            return {"modified_count": result.modified_count}
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
       
    def _get_conferenceroom_booking(self,Cluster_ID:str,room_id:str):
        try:
            result = self.conferenceRoom_collection.find_one({"cluster_id": Cluster_ID,"buildings.id": int(room_id)}, {"buildings.$": 1, "_id": 0})
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    