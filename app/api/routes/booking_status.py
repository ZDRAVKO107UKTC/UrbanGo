from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.events import EventBus
from app.repositories.booking_status_repo import BookingStatusRepository, NotFoundError, ConflictError

router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_event_bus() -> EventBus:
    from app.main import event_bus
    return event_bus

@router.patch("/{booking_id}/ready", status_code=200)
def mark_booking_ready(
    booking_id: int,
    db: Session = Depends(get_db),
):
    repo = BookingStatusRepository(db)
    try:
        event = repo.mark_ready_and_emit(booking_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

    bus = get_event_bus()
    bus.publish("BOOKING_READY", event.payload)

    return {"booking_id": event.booking_id, "status": "READY"}
