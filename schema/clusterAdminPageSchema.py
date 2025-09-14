from typing import Optional
from pydantic import BaseModel

class ConferenceRoom(BaseModel):
    id: Optional[int]
    BuildingName: str
    Floor: str
    ConferenceRoomType: str
    ConferenceRoomName: str
    Capacity: int
    isAvailable: bool
    imageUrl: Optional[str]

class RoomStatusUpdate(BaseModel):
    isAvailable: bool 