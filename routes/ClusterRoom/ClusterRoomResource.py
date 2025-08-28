from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Header
from fastapi_utils.cbv import cbv

from service.ClusterRoom.ClusterRoomService import ClusterRoomService


clusterroom_resourse = APIRouter()


@cbv(clusterroom_resourse)
class ClusterRoomResourse:
    def __init__(self, clusterRoomService: ClusterRoomService = Depends()):
        self.clusterRoomService=clusterRoomService

   

       