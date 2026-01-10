from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.booking import BookingOut
from app.repositories.booking_complete_repo import (
    BookingCompleteRepository, NotFoundError, ConflictError, ForbiddenError, BadRequestError
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.patch("/{booking_id}/complete", response_model=BookingOut, status_code=200)
def complete_booking(
    booking_id: int,
    driver_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    repo = BookingCompleteRepository(db)
    try:
        return repo.complete_booking(booking_id=booking_id, driver_id=driver_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
