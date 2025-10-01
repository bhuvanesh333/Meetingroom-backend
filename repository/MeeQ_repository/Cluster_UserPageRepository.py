from database.dataBase_Initializer import ConferenceRoom_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ClusterUserPageRepository:

    def __init__(self):
        self.conferenceRoom_collection = ConferenceRoom_collection

    def _get_all_booking_list(self,Cluster_ID:str):
        try:
            result = self.conferenceRoom_collection.find_one({"Cluster_ID": Cluster_ID},  
                                        {"Buildings": 1, "_id": 0} )
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _get_conferenceroom_booking(self,Cluster_ID:str,room_id:str):
        try:
            result = self.conferenceRoom_collection.find_one({"Cluster_ID": Cluster_ID,"Buildings.id": int(room_id)}, {"Buildings.$": 1, "_id": 0})
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    