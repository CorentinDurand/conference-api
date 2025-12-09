from typing import List

from fastapi import APIRouter

from models import Room, RoomCreate, RoomUpdate
from services import rooms as rooms_service
from dependencies import require_role

router = APIRouter(prefix="/api/v1/rooms", tags=["rooms"])


@router.get("", response_model=List[Room], dependencies=[require_role("admin", "event_manager", "viewer")])
def list_rooms():
    return rooms_service.list_rooms()


@router.post("", response_model=Room, status_code=201, dependencies=[require_role("admin")])
def create_room(room: RoomCreate):
    return rooms_service.create_room(room)


@router.get("/{room_id}", response_model=Room, dependencies=[require_role("admin", "event_manager", "viewer")])
def get_room(room_id: int):
    return rooms_service.get_room(room_id)


@router.patch("/{room_id}", response_model=Room, dependencies=[require_role("admin")])
def update_room(room_id: int, room: RoomUpdate):
    return rooms_service.update_room(room_id, room)


@router.delete("/{room_id}", status_code=204, dependencies=[require_role("admin")])
def delete_room(room_id: int):
    rooms_service.delete_room(room_id)
    return None
