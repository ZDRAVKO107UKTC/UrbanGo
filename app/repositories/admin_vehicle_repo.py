from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.models.vehicle import Vehicle

class NotFoundError(Exception):
    pass

class BadRequestError(Exception):
    pass

class AdminVehicleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_vehicle(self, admin_id: int, vehicle_type: str, plate_number: str | None, model: str) -> Vehicle:
        admin = self.db.execute(select(User).where(User.id == admin_id)).scalar_one_or_none()
        if admin is None:
            raise NotFoundError("Admin not found")
        if admin.role != "ADMIN":
            raise BadRequestError("User is not an admin")

        vehicle = Vehicle(
            vehicle_type=vehicle_type,
            plate_number=plate_number,
            model=model,
            status="AVAILABLE",
            available=True,
        )

        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
