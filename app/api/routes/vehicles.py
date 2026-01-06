from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.vehicle_repo import VehicleRepository

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

VALID_TYPES = {"CAR", "SCOOTER", "BIKE"}

@router.get("", status_code=200)
def list_vehicles(
    vehicle_type: str | None = Query(default=None, alias="type"),
    db: Session = Depends(get_db),
):
    if vehicle_type is not None:
        vt = vehicle_type.strip().upper()
        if vt not in VALID_TYPES:
            raise HTTPException(status_code=400, detail="Invalid vehicle type. Use CAR, SCOOTER, or BIKE.")
        vehicle_type = vt

    repo = VehicleRepository(db)
    return repo.list_available(vehicle_type)
