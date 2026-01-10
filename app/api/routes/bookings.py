from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.repositories.booking_repo import BookingRepository, NotFoundError as BookingNotFoundError, ConflictError
from app.repositories.booking_pending_repo import BookingPendingRepository, NotFoundError as DriverNotFoundError, BadRequestError

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    try:
        return repo.create_booking_transactional(
            rider_id=payload.rider_id,
            vehicle_id=payload.vehicle_id,
        )
    except BookingNotFoundError:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    except ConflictError:
        raise HTTPException(status_code=409, detail="Vehicle is not available")

@router.get("/pending", response_model=list[BookingOut], status_code=200)
def get_pending_bookings(
    driver_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    repo = BookingPendingRepository(db)
    try:
        return repo.list_pending_for_driver(driver_id)
    except DriverNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
