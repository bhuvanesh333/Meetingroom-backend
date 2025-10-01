
import json
import time
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException, Header

from schema.commonSchema import APIResponse
from service.MeeQ_service.Cluster_UserPageService import ClusterUserPageService

cluster_user_page_resourse = APIRouter()


@cbv(cluster_user_page_resourse)
class ClusterUserPageResourse:

    def __init__(self,clusterUserPageService:ClusterUserPageService= Depends()):
        self.clusterUserPageService=clusterUserPageService

    @cluster_user_page_resourse.get("/ClusterUserGetAllBoking",response_model=APIResponse)
    def cluster_user_get_all_booking(self,Cluster_ID: str = Header(..., alias="X-Cluster_ID")):
        if not Cluster_ID:
            raise HTTPException(status_code=400, detail="X-Cluster_ID header is required")
        return self.clusterUserPageService.get_all_booking_list(Cluster_ID)
    
    # Generator function to stream events
    def event_stream(self, cluster_id: str, room_id: str):
        while True:
            try:
                result = self.clusterUserPageService.stream_conference_room_to(cluster_id, room_id)
                yield f"data: {json.dumps(result)}\n\n"
            except HTTPException as e:
                yield f"data: ERROR: {e.detail}\n\n"
            except Exception as e:
                yield f"data: ERROR: {str(e)}\n\n"
            
            time.sleep(10)

    @cluster_user_page_resourse.get("/stream")
    def stream(self, cluster_id: str, room_id: str):
        return StreamingResponse(self.event_stream(cluster_id, room_id), media_type="text/event-stream")