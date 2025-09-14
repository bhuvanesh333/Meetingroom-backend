
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, Header

from schema.clusterAdminPageSchema import ConferenceRoom, RoomStatusUpdate
from schema.commonSchema import APIResponse
from service.MeeQ_service.Cluster_AdminPageService import ClusterAdminPageService



cluster_admin_page_resourse = APIRouter()


@cbv(cluster_admin_page_resourse)
class ClusterAdminPageResourse:

    def __init__(self,clusterAdminPageService:ClusterAdminPageService= Depends()):
        self.clusterAdminPageService=clusterAdminPageService
    
    @cluster_admin_page_resourse.post("/addClusterConferenceRoom",response_model=APIResponse)
    def cluster_add_conferenceroom(self,conferenceRoom_data:ConferenceRoom,
                                Cluster_ID: str = Header(..., alias="X-Cluster_ID")):
        return self.clusterAdminPageService.add_cluster_conferenceroom(conferenceRoom_data,Cluster_ID)
    
    @cluster_admin_page_resourse.get("/getClusterConferenceRoom",response_model=APIResponse)
    def cluster_get_conferenceroom(self,Cluster_ID: str = Header(..., alias="X-Cluster_ID")):
        return self.clusterAdminPageService.get_cluster_conferenceroom(Cluster_ID)
    
    @cluster_admin_page_resourse.delete("/deleteClusterConferenceRoom",response_model=APIResponse)
    def cluster_delete_conferenceroom(self,Cluster_ID: str = Header(..., alias="X-Cluster_ID"),Room_ID: int = Header(..., alias="X-Room_ID")):
        return self.clusterAdminPageService.delete_cluster_conferenceroom(Room_ID,Cluster_ID)
    

    @cluster_admin_page_resourse.put("/updateClusterRoomAvailability",response_model=APIResponse)
    def cluster_update_avail_conferenceroom(self,room_status:RoomStatusUpdate,Cluster_ID: str = Header(..., alias="X-Cluster_ID"),Room_ID: int = Header(..., alias="X-Room_ID")):
        return self.clusterAdminPageService.update_clusterroom_avail_conferenceroom(Room_ID,Cluster_ID,room_status)

    @cluster_admin_page_resourse.put("/updateClusterConferenceRoom",response_model=APIResponse)
    def cluster_update_conferenceroom(self,conferenceRoom_data:ConferenceRoom,
                                Cluster_ID: str = Header(..., alias="X-Cluster_ID")):
        return self.clusterAdminPageService.update_cluster_conferenceroom(conferenceRoom_data,Cluster_ID)