# Conference Room Booking API

## Prerequisites
- Python 3.10+ installed.
- `pip` available.
- Optional: create and activate a virtual environment (`python -m venv venv` then activate it).

## Setup
```bash
pip install fastapi uvicorn
```
Using the virtual environment on Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn
```

## Run the API and open Swagger UI
```bash
uvicorn main:app --reload
```
- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Healthcheck: `http://127.0.0.1:8000/health`

## Main resources
- `/api/v1/rooms`: rooms CRUD
- `/api/v1/bookings`: bookings CRUD
- `/api/v1/events`: events CRUD

## Roles and route access (expected)
Auth is header-based: send `X-User-Role` with one of `admin`, `event_manager`, or `viewer`.
- Viewer: read-only access on rooms, bookings, events.
- Event Manager: full CRUD on bookings and events; read-only on rooms.
- Admin: full CRUD on rooms, bookings, events.
