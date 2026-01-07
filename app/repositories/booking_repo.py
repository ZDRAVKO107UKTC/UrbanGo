from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.vehicle import Vehicle
from app.models.booking import Booking

class NotFoundError(Exception):
    pass

class ConflictError(Exception):
    pass

class BookingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_booking_transactional(self, rider_id: int, vehicle_id: int) -> Booking:
        # One atomic unit of work
        with self.db.begin():
            vehicle = self.db.execute(
                select(Vehicle)
                .where(Vehicle.id == vehicle_id)
                .with_for_update()
            ).scalar_one_or_none()

            if vehicle is None:
                raise NotFoundError("Vehicle not found")

            if not vehicle.available:
                raise ConflictError("Vehicle is not available")

            booking = Booking(
                rider_id=rider_id,
                driver_id=None,
                vehicle_id=vehicle_id,
                status="REQUESTED",
            )
            self.db.add(booking)
            self.db.flush()

            vehicle.available = False
            vehicle.status = "UNAVAILABLE"

            return booking
