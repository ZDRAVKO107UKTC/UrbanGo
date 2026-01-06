from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.vehicle import Vehicle

VALID_TYPES = {"CAR", "SCOOTER", "BIKE"}

class VehicleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_available(self, vehicle_type: str | None) -> list[Vehicle]:
        stmt = select(Vehicle).where(Vehicle.available.is_(True))

        if vehicle_type:
            vt = vehicle_type.strip().upper()
            if vt not in VALID_TYPES:
                raise ValueError("Invalid vehicle type")
            stmt = stmt.where(Vehicle.vehicle_type == vt)

        result = self.db.execute(stmt).scalars().all()
        return result
