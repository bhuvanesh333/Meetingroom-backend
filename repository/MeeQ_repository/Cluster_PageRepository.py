from fastapi import HTTPException
from database.dataBase_Initializer import ConferenceRoom_collection
from schema.clusterAdminPageSchema import ConferenceRoom
from pymongo.errors import PyMongoError

class ClusterPageRepository:

    def __init__(self):
        self.conferenceRoom_collection = ConferenceRoom_collection

    def _get_all_building_id(self, Cluster_ID: str):
        try:
            cluster = self.conferenceRoom_collection.find_one(
                {"Cluster_ID": Cluster_ID},
                {"Buildings.id": 1}
            )
            if not cluster:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return cluster
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _get_all_building(self,Cluster_ID: str):
        try:
            cluster = self.conferenceRoom_collection.find_one(
                {"Cluster_ID": Cluster_ID},
                {"Buildings": 1}
            )
            if not cluster:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return cluster
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _set_conference_room_by_fields(self, conferenceRoom_data: dict, Cluster_ID: str):
        try:
            result = self.conferenceRoom_collection.update_one(
                {"Cluster_ID": Cluster_ID},
                {"$push": {"Buildings": conferenceRoom_data}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _update_conference_room_by_fields(self, conferenceRoom_data: dict, Cluster_ID: str):
        try:
            result = self.conferenceRoom_collection.update_one(
                {"Cluster_ID": Cluster_ID,"Buildings.id": conferenceRoom_data["id"]}, 
                {"$set": {"Buildings.$": conferenceRoom_data}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _delete_building_by_Room_Id(self,Room_ID:int,Cluster_ID:str):
        try:
            result = self.conferenceRoom_collection.update_one(
                {"Cluster_ID": Cluster_ID}, 
                { "$pull": { "Buildings": { "id": Room_ID } } }
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _update_building_roomstatus(self,Room_ID:int,Cluster_ID:str,room_status):
        try:
            result = self.conferenceRoom_collection.update_one(
                {"Cluster_ID": Cluster_ID,"Buildings.id": Room_ID}, 
                {"$set": {"Buildings.$.isAvailable": room_status["isAvailable"]} }
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Cluster not found")
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        