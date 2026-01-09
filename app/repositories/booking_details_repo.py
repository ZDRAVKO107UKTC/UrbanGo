from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.booking import Booking

class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class BookingDetailsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_booking_for_rider(self, booking_id: int, rider_id: int) -> Booking:
        booking = self.db.execute(
            select(Booking).where(Booking.id == booking_id)
        ).scalar_one_or_none()

        if booking is None:
            raise NotFoundError("Booking not found")

        if booking.rider_id != rider_id:
            raise ForbiddenError("Booking does not belong to rider")

        return booking
