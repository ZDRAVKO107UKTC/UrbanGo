from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.repositories.booking_repo import BookingRepository, NotFoundError, ConflictError

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    try:
        booking = repo.create_booking_transactional(
            rider_id=payload.rider_id,
            vehicle_id=payload.vehicle_id,
        )
        return booking
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    except ConflictError:
        raise HTTPException(status_code=409, detail="Vehicle is not available")
