from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.vehicle_repo import VehicleRepository
from app.schemas.vehicle import VehicleOut

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("", response_model=list[VehicleOut], status_code=200)
def list_vehicles(
    type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    repo = VehicleRepository(db)
    try:
        return repo.list_available(type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid vehicle type. Use CAR, SCOOTER, or BIKE.")
