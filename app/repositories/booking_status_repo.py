from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import func

from app.models.booking import Booking
from app.models.outbox import BookingEventOutbox

class NotFoundError(Exception):
    pass

class ConflictError(Exception):
    pass

class BookingStatusRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def mark_ready_and_emit(self, booking_id: int) -> BookingEventOutbox:
        with self.db.begin():
            booking = self.db.execute(
                select(Booking).where(Booking.id == booking_id).with_for_update()
            ).scalar_one_or_none()

            if booking is None:
                raise NotFoundError("Booking not found")

            if booking.status != "ACCEPTED":
                raise ConflictError("Booking must be ACCEPTED before READY")

            booking.status = "READY"
            booking.ready_at = func.now()

            payload = {
                "booking_id": booking.id,
                "rider_id": booking.rider_id,
                "driver_id": booking.driver_id,
                "vehicle_id": booking.vehicle_id,
                "status": "READY",
            }

            event = BookingEventOutbox(
                booking_id=booking.id,
                event_type="BOOKING_READY",
                payload=payload,
            )
            self.db.add(event)
            self.db.flush()
            return event
