from typing import List, Optional
from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    name: str
    building: str
    floor: int
    capacity: int = Field(gt=0)
    features: List[str] = Field(default_factory=list)
    defaultTableSetting: str = "BOARDROOM"


class Room(RoomCreate):
    id: int


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    features: Optional[List[str]] = None
    defaultTableSetting: Optional[str] = None
