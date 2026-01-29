from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.booking import Booking
from sqlalchemy.orm import joinedload

class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class BookingDetailsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_booking_for_rider(self, booking_id: int, rider_id: int) -> Booking:
        booking = self.db.execute(
            select(Booking)
            .options(joinedload(Booking.driver), joinedload(Booking.vehicle))
            .where(Booking.id == booking_id, Booking.rider_id == rider_id)
        ).scalar_one_or_none()

        if booking is None:
            raise NotFoundError("Booking not found")


        return booking
