from datetime import time
from typing import Dict, Optional

from fastapi import HTTPException

from models import Room, Booking, BookingCreate, Event


# ===== In-memory "DB" =====

rooms: Dict[int, Room] = {}
bookings: Dict[int, Booking] = {}
events: Dict[int, Event] = {}

next_room_id = 1
next_booking_id = 1
next_event_id = 1


def reset_storage():
    """Utile pour des tests si besoin."""
    global rooms, bookings, events, next_room_id, next_booking_id, next_event_id
    rooms = {}
    bookings = {}
    events = {}
    next_room_id = 1
    next_booking_id = 1
    next_event_id = 1


# ===== common Helpers =====

def check_room_exists(room_id: int) -> Room:
    room = rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def check_booking_exists(booking_id: int) -> Booking:
    booking = bookings.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


def check_event_exists(event_id: int) -> Event:
    event = events.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


def times_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    return start1 < end2 and start2 < end1


def validate_booking_slot(new: BookingCreate, ignore_booking_id: Optional[int] = None):
    """Vérifie capacité, cohérence des horaires et conflits de créneaux."""
    room = check_room_exists(new.roomId)

    if new.startTime >= new.endTime:
        raise HTTPException(status_code=400, detail="startTime must be before endTime")

    if new.numberOfPeople > room.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"numberOfPeople ({new.numberOfPeople}) exceeds room capacity ({room.capacity})",
        )

    for b in bookings.values():
        if ignore_booking_id is not None and b.id == ignore_booking_id:
            continue
        if b.roomId == new.roomId and b.date == new.date and b.status == "CONFIRMED":
            if times_overlap(new.startTime, new.endTime, b.startTime, b.endTime):
                raise HTTPException(
                    status_code=409,
                    detail=f"Time slot conflicts with booking {b.id}",
                )


# ===== Deletes =====

def delete_room(room_id: int):
    room = check_room_exists(room_id)
    has_bookings = any(b.roomId == room_id for b in bookings.values())
    if has_bookings:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete room with existing bookings",
        )
    del rooms[room_id]
    return room


def delete_booking(booking_id: int):
    booking = check_booking_exists(booking_id)
    if booking.eventId is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete booking belonging to an event. Cancel or delete the event instead.",
        )
    del bookings[booking_id]
    return booking


def delete_event(event_id: int):
    event = check_event_exists(event_id)
    for b_id in list(event.bookingIds):
        bookings.pop(b_id, None)
    del events[event_id]
    return event
