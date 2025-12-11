from bson import ObjectId
from database.dataBase_Initializer import Clusteruser_auth_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ClusterUserRepository:

    def __init__(self):
        self.clusteruser_auth_collection = Clusteruser_auth_collection

    def _set_active_status(self,user_id:str,is_active:bool):
        try:
            result = self.clusteruser_auth_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": is_active}}
            )
            return result.modified_count
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _get_cluster_user_by_fields(self,field_name_value):
        try:
            result = self.clusteruser_auth_collection.find_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    def _set_cluster_user_by_fields(self,field_name_value):
        try:
            result = self.clusteruser_auth_collection.insert_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")