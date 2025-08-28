from database.dataBase_Initializer import Clusterroom_auth_collection

class ClusterRoomAuthRepository:
    def __init__(self):
        self.clusterroom_auth_collection = Clusterroom_auth_collection 
    
    def _get_clusterroom_cluster_user_field(self,  field_name_value:dict):
        result = self.clusterroom_auth_collection.find_one(field_name_value)
        return result