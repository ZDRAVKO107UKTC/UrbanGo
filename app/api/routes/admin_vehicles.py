from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.authz import require_role
from app.schemas.admin_vehicle import VehicleCreate
from app.schemas.vehicle import VehicleOut
from app.repositories.admin_vehicle_repo import AdminVehicleRepository

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/vehicles", response_model=VehicleOut, status_code=201)
def admin_create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_role("ADMIN")),
):
    repo = AdminVehicleRepository(db)
    return repo.create_vehicle(
        admin_id=admin_id,
        vehicle_type=payload.vehicle_type,
        plate_number=payload.plate_number,
        model=payload.model,
    )
