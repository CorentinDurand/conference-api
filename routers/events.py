from typing import List

from fastapi import APIRouter

from models import Event, EventCreate, EventStatusUpdate, Booking
from services import events as events_service
from dependencies import require_role

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.get("", response_model=List[Event], dependencies=[require_role("admin", "event_manager", "viewer")])
def list_events():
    return events_service.list_events()


@router.get("/{event_id}", response_model=Event, dependencies=[require_role("admin", "event_manager", "viewer")])
def get_event(event_id: int):
    return events_service.get_event(event_id)


@router.get("/{event_id}/bookings", response_model=List[Booking], dependencies=[require_role("admin", "event_manager", "viewer")])
def get_event_bookings(event_id: int):
    return events_service.get_event_bookings(event_id)


@router.post("", response_model=Event, status_code=201, dependencies=[require_role("admin", "event_manager")])
def create_event(event: EventCreate):
    return events_service.create_event(event)


@router.patch("/{event_id}", response_model=Event, dependencies=[require_role("admin", "event_manager")])
def cancel_event(event_id: int, update: EventStatusUpdate):
    return events_service.cancel_event(event_id, update)


@router.delete("/{event_id}", status_code=204, dependencies=[require_role("admin", "event_manager")])
def delete_event(event_id: int):
    events_service.delete_event(event_id)
    return None
