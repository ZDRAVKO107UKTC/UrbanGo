from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import func

from app.models.booking import Booking
from app.models.user import User

class NotFoundError(Exception):
    pass

class ConflictError(Exception):
    pass

class BadRequestError(Exception):
    pass

class BookingAcceptRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def accept_booking(self, booking_id: int, driver_id: int) -> Booking:
        with self.db.begin():
            driver = self.db.execute(
                select(User).where(User.id == driver_id)
            ).scalar_one_or_none()

            if driver is None:
                raise NotFoundError("Driver not found")

            if driver.role != "DRIVER":
                raise BadRequestError("User is not a driver")

            if not driver.driver_available:
                raise BadRequestError("Driver is not available")

            booking = self.db.execute(
                select(Booking)
                .where(Booking.id == booking_id)
                .with_for_update()
            ).scalar_one_or_none()

            if booking is None:
                raise NotFoundError("Booking not found")

            if booking.status != "REQUESTED":
                raise ConflictError("Booking is not in REQUESTED state")

            booking.driver_id = driver_id
            booking.status = "ACCEPTED"
            booking.accepted_at = func.now()

            self.db.flush()
            return booking
