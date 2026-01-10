from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.booking import Booking

class AdminBookingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all_bookings(self, status: str | None = None) -> list[Booking]:
        stmt = select(Booking)

        if status is not None:
            stmt = stmt.where(Booking.status == status)

        stmt = stmt.order_by(Booking.id.desc())

        return self.db.execute(stmt).scalars().all()
