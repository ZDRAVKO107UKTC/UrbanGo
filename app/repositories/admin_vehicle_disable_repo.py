from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.vehicle import Vehicle

class NotFoundError(Exception):
    pass

class ConflictError(Exception):
    pass

class AdminVehicleDisableRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def disable_vehicle(self, vehicle_id: int) -> Vehicle:
        vehicle = self.db.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        ).scalar_one_or_none()

        if vehicle is None:
            raise NotFoundError("Vehicle not found")

        if vehicle.status != "AVAILABLE" and vehicle.available is False:
            raise ConflictError("Vehicle already disabled")

        vehicle.status = "MAINTENANCE"
        vehicle.available = False

        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
