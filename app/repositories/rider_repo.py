from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.booking import Booking

class NotFoundError(Exception):
    pass

class RiderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_booking_history(self, rider_id: int) -> list[Booking]:
        rider = self.db.execute(
            select(User).where(User.id == rider_id)
        ).scalar_one_or_none()

        if rider is None:
            raise NotFoundError("Rider not found")

        if rider.role != "RIDER":
            raise NotFoundError("Rider not found")

        bookings = self.db.execute(
            select(Booking)
            .where(Booking.rider_id == rider_id)
            .order_by(Booking.id.desc())
        ).scalars().all()

        return bookings
