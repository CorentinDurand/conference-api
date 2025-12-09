from datetime import date, time
from typing import Optional, Literal
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    roomId: int
    date: date
    startTime: time
    endTime: time
    numberOfPeople: int = Field(gt=0)
    tableSetting: str = "BOARDROOM"
    notes: Optional[str] = None


class BookingUpdate(BaseModel):
    date: Optional[date] = None
    startTime: Optional[time] = None
    endTime: Optional[time] = None
    numberOfPeople: Optional[int] = Field(default=None, gt=0)
    tableSetting: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[Literal["CONFIRMED", "CANCELLED"]] = None


class Booking(BookingCreate):
    id: int
    status: Literal["CONFIRMED", "CANCELLED"] = "CONFIRMED"
    eventId: Optional[int] = None
