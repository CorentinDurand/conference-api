from fastapi import FastAPI

from routers import rooms, bookings, events

app = FastAPI(title="Conference Room Booking API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(events.router)