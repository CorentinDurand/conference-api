from typing import List

from fastapi import HTTPException

from models import Booking, BookingCreate, BookingUpdate
import storage


def list_bookings() -> List[Booking]:
    return list(storage.bookings.values())


def create_booking(booking_in: BookingCreate) -> Booking:
    storage.validate_booking_slot(booking_in)

    booking_id = storage.next_booking_id
    storage.next_booking_id += 1

    booking = Booking(
        id=booking_id,
        **booking_in.dict(),
        status="CONFIRMED",
        eventId=None,
    )
    storage.bookings[booking_id] = booking
    return booking


def get_booking(booking_id: int) -> Booking:
    return storage.check_booking_exists(booking_id)


def update_booking(booking_id: int, update: BookingUpdate) -> Booking:
    existing = storage.check_booking_exists(booking_id)

    if existing.eventId is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot modify booking belonging to an event. Cancel the event instead.",
        )

    data = existing.dict()
    for field, value in update.dict(exclude_unset=True).items():
        data[field] = value

    from models import BookingCreate as BC
    maybe_new = BC(
        roomId=data["roomId"],
        date=data["date"],
        startTime=data["startTime"],
        endTime=data["endTime"],
        numberOfPeople=data["numberOfPeople"],
        tableSetting=data["tableSetting"],
        notes=data["notes"],
    )
    storage.validate_booking_slot(maybe_new, ignore_booking_id=booking_id)

    updated = Booking(**data)
    storage.bookings[booking_id] = updated
    return updated


def delete_booking(booking_id: int):
    return storage.delete_booking(booking_id)
