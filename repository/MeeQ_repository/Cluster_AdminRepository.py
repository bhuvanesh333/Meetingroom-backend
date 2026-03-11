from bson import ObjectId
from database.dataBase_Initializer import Clusteradmin_auth_collection, ConferenceRoom_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ClusterAdminRepository:

    def __init__(self):
        self.clusteradmin_auth_collection = Clusteradmin_auth_collection
        self.conferenceRoom_collection = ConferenceRoom_collection

    def _get_cluster_admin_by_fields(self, field_name_value: dict):
        try:
            result = self.clusteradmin_auth_collection.find_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _set_active_status(self,user_id:str,is_online:bool):
        try:
            result = self.clusteradmin_auth_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_online": is_online}}
            )
            return result.modified_count
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _set_cluster_admin_by_fields(self, field_name_value: dict):
        try:
            result = self.clusteradmin_auth_collection.insert_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def create_conference_room(self,field_name_value: dict):
        try:
            result = self.conferenceRoom_collection.insert_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")