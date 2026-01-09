from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingOut
from app.repositories.rider_repo import RiderRepository, NotFoundError

router = APIRouter(prefix="/riders", tags=["riders"])

@router.get("/{rider_id}/bookings", response_model=list[BookingOut], status_code=200)
def get_rider_booking_history(rider_id: int, db: Session = Depends(get_db)):
    repo = RiderRepository(db)
    try:
        return repo.list_booking_history(rider_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
