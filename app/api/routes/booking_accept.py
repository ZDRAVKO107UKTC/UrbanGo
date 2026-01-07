from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingOut
from app.repositories.booking_accept_repo import (
    BookingAcceptRepository, NotFoundError, ConflictError, BadRequestError
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.patch("/{booking_id}/accept", response_model=BookingOut, status_code=200)
def accept_booking(booking_id: int, driver_id: int, db: Session = Depends(get_db)):
    repo = BookingAcceptRepository(db)
    try:
        return repo.accept_booking(booking_id=booking_id, driver_id=driver_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
