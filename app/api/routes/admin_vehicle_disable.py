from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.authz import require_role
from app.schemas.vehicle import VehicleOut
from app.repositories.admin_vehicle_disable_repo import (
    AdminVehicleDisableRepository,
    NotFoundError,
    ConflictError,
)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.patch("/vehicles/{vehicle_id}/disable", response_model=VehicleOut, status_code=200)
def admin_disable_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_role("ADMIN")),
):
    repo = AdminVehicleDisableRepository(db)
    try:
        return repo.disable_vehicle(vehicle_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
