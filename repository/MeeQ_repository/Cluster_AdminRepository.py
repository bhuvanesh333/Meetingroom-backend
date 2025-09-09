from database.dataBase_Initializer import Clusterroom_auth_collection

class ClusterAdminRepository:

    def __init__(self):
        self.clusterAuthCollection = Clusterroom_auth_collection

    def _get_cluster_admin_by_fiels(self,  field_name_value:dict):
        result = self.clusterAuthCollection.find_one(field_name_value)
        return result

