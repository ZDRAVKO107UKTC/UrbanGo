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

class ForbiddenError(Exception):
    pass

class BadRequestError(Exception):
    pass

class BookingCompleteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def complete_booking(self, booking_id: int, driver_id: int) -> Booking:
        with self.db.begin():
            driver = self.db.execute(
                select(User).where(User.id == driver_id)
            ).scalar_one_or_none()

            if driver is None:
                raise NotFoundError("Driver not found")

            if driver.role != "DRIVER":
                raise BadRequestError("User is not a driver")

            booking = self.db.execute(
                select(Booking)
                .where(Booking.id == booking_id)
                .with_for_update()
            ).scalar_one_or_none()

            if booking is None:
                raise NotFoundError("Booking not found")

            if booking.driver_id != driver_id:
                raise ForbiddenError("Booking is not assigned to this driver")

            if booking.status != "READY":
                raise ConflictError("Booking must be READY before COMPLETED")

            booking.status = "COMPLETED"
            booking.completed_at = func.now()

            self.db.flush()
            return booking
