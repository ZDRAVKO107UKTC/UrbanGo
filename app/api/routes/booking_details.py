from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingOut
from app.repositories.booking_details_repo import (
    BookingDetailsRepository, NotFoundError, ForbiddenError
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/{booking_id}", response_model=BookingOut, status_code=200)
def get_booking_details(
    booking_id: int,
    rider_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    repo = BookingDetailsRepository(db)
    try:
        return repo.get_booking_for_rider(booking_id=booking_id, rider_id=rider_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
