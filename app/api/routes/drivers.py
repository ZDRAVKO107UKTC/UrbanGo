from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.driver import DriverAvailabilityUpdate, DriverAvailabilityOut
from app.repositories.driver_repo import DriverRepository, NotFoundError, BadRequestError

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.patch("/{driver_id}/availability", response_model=DriverAvailabilityOut, status_code=200)
def update_driver_availability(
    driver_id: int,
    payload: DriverAvailabilityUpdate,
    db: Session = Depends(get_db),
):
    repo = DriverRepository(db)
    try:
        return repo.set_availability(driver_id=driver_id, available=payload.driver_available)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Driver not found")
    except BadRequestError:
        raise HTTPException(status_code=400, detail="User is not a driver")
