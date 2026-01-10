from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.booking import Booking

class NotFoundError(Exception):
    pass

class BadRequestError(Exception):
    pass

class BookingPendingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_pending_for_driver(self, driver_id: int) -> list[Booking]:
        driver = self.db.execute(
            select(User).where(User.id == driver_id)
        ).scalar_one_or_none()

        if driver is None:
            raise NotFoundError("Driver not found")

        if driver.role != "DRIVER":
            raise BadRequestError("User is not a driver")

        pending = self.db.execute(
            select(Booking)
            .where(Booking.status == "REQUESTED")
            .order_by(Booking.id.desc())
        ).scalars().all()

        return pending
