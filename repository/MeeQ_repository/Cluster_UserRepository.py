from database.dataBase_Initializer import Clusteruser_auth_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ClusterUserRepository:

    def __init__(self):
        self.clusteruser_auth_collection = Clusteruser_auth_collection

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