from typing import List

from fastapi import APIRouter

from models import Booking, BookingCreate, BookingUpdate
from services import bookings as bookings_service
from dependencies import require_role

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.get("", response_model=List[Booking], dependencies=[require_role("admin", "event_manager", "viewer")])
def list_bookings():
    return bookings_service.list_bookings()


@router.post("", response_model=Booking, status_code=201, dependencies=[require_role("admin", "event_manager")])
def create_booking(booking: BookingCreate):
    return bookings_service.create_booking(booking)


@router.get("/{booking_id}", response_model=Booking, dependencies=[require_role("admin", "event_manager", "viewer")])
def get_booking(booking_id: int):
    return bookings_service.get_booking(booking_id)


@router.patch("/{booking_id}", response_model=Booking, dependencies=[require_role("admin", "event_manager")])
def update_booking(booking_id: int, update: BookingUpdate):
    return bookings_service.update_booking(booking_id, update)


@router.delete("/{booking_id}", status_code=204, dependencies=[require_role("admin", "event_manager")])
def delete_booking(booking_id: int):
    bookings_service.delete_booking(booking_id)
    return None
