from typing import List

from fastapi import HTTPException

from models import Event, EventCreate, EventStatusUpdate, Booking, BookingCreate
import storage


def list_events() -> List[Event]:
    return list(storage.events.values())


def get_event(event_id: int) -> Event:
    return storage.check_event_exists(event_id)


def get_event_bookings(event_id: int) -> List[Booking]:
    event = storage.check_event_exists(event_id)
    return [storage.bookings[b_id] for b_id in event.bookingIds]


def create_event(event_in: EventCreate) -> Event:
    if event_in.startDate > event_in.endDate:
        raise HTTPException(status_code=400, detail="startDate must be before endDate")

    event_id = storage.next_event_id
    storage.next_event_id += 1

    event = Event(
        id=event_id,
        name=event_in.name,
        description=event_in.description,
        startDate=event_in.startDate,
        endDate=event_in.endDate,
        organizerUserId=event_in.organizerUserId,
        status="PLANNED",
        bookingIds=[],
    )

    for day in event_in.days:
        if day.date < event_in.startDate or day.date > event_in.endDate:
            raise HTTPException(
                status_code=400,
                detail=f"Day {day.date} is outside event date range",
            )

        booking_create = BookingCreate(
            roomId=day.roomId,
            date=day.date,
            startTime=day.startTime,
            endTime=day.endTime,
            numberOfPeople=day.numberOfPeople,
            tableSetting=day.tableSetting,
            notes=f"Event {event_id}: {event_in.name}",
        )

        storage.validate_booking_slot(booking_create)

        booking_id = storage.next_booking_id
        storage.next_booking_id += 1

        booking = Booking(
            id=booking_id,
            **booking_create.dict(),
            status="CONFIRMED",
            eventId=event_id,
        )
        storage.bookings[booking_id] = booking
        event.bookingIds.append(booking_id)

    storage.events[event_id] = event
    return event


def cancel_event(event_id: int, update: EventStatusUpdate) -> Event:
    event = storage.check_event_exists(event_id)

    if update.status != "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Only status=CANCELLED is allowed for events",
        )

    event.status = "CANCELLED"
    storage.events[event_id] = event

    for b_id in event.bookingIds:
        booking = storage.bookings[b_id]
        booking.status = "CANCELLED"
        storage.bookings[b_id] = booking

    return event


def delete_event(event_id: int):
    return storage.delete_event(event_id)
