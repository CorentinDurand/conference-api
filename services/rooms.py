from typing import List

from fastapi import HTTPException

from models import Room, RoomCreate, RoomUpdate
import storage


def list_rooms() -> List[Room]:
    return list(storage.rooms.values())


def create_room(room_in: RoomCreate) -> Room:
    room_id = storage.next_room_id
    storage.next_room_id += 1

    room = Room(id=room_id, **room_in.dict())
    storage.rooms[room_id] = room
    return room


def get_room(room_id: int) -> Room:
    return storage.check_room_exists(room_id)


def update_room(room_id: int, room_in: RoomUpdate) -> Room:
    existing = storage.check_room_exists(room_id)
    data = existing.dict()
    updates = room_in.dict(exclude_unset=True)

    if "capacity" in updates:
        new_capacity = updates["capacity"]
        has_too_large_booking = any(
            b.roomId == room_id and b.numberOfPeople > new_capacity
            for b in storage.bookings.values()
        )
        if has_too_large_booking:
            raise HTTPException(
                status_code=409,
                detail="Cannot reduce capacity below existing bookings' numberOfPeople",
            )

    data.update(updates)
    updated = Room(**data)
    storage.rooms[room_id] = updated
    return updated


def delete_room(room_id: int) -> Room:
    return storage.delete_room(room_id)
