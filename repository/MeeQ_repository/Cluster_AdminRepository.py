from database.dataBase_Initializer import Clusterroom_auth_collection
from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ClusterAdminRepository:

    def __init__(self):
        self.clusterAuthCollection = Clusterroom_auth_collection

    def _get_cluster_admin_by_fields(self, field_name_value: dict):
        try:
            result = self.clusterAuthCollection.find_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _set_cluster_admin_by_fields(self, field_name_value: dict):
        try:
            result = self.clusterAuthCollection.insert_one(field_name_value)
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
