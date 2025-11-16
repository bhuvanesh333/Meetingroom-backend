from typing import Optional
from pydantic import BaseModel

class ConferenceRoom(BaseModel):
    id: Optional[int]
    building_name: str
    floor: str
    conference_room_type: str
    conference_room_name: str
    capacity: int
    is_available: bool
    image_url: Optional[str]

class RoomStatusUpdate(BaseModel):
    is_available: bool 