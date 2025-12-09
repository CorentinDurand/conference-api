from datetime import date, time
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class EventDay(BaseModel):
    date: date
    roomId: int
    startTime: time
    endTime: time
    numberOfPeople: int = Field(gt=0)
    tableSetting: str = "BOARDROOM"


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    startDate: date
    endDate: date
    organizerUserId: str
    days: List[EventDay]


class EventStatusUpdate(BaseModel):
    status: Literal["CANCELLED"]


class Event(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    startDate: date
    endDate: date
    organizerUserId: str
    status: Literal["PLANNED", "CANCELLED"] = "PLANNED"
    bookingIds: List[int] = Field(default_factory=list)
