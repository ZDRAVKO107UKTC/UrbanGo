from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.authz import require_role
from app.schemas.booking import BookingOut
from app.repositories.admin_booking_repo import AdminBookingRepository

router = APIRouter(prefix="/admin", tags=["admin"])

ALLOWED_STATUSES = {"REQUESTED", "ACCEPTED", "READY", "COMPLETED"}

@router.get("/bookings", response_model=list[BookingOut], status_code=200)
def admin_list_bookings(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_role("ADMIN")),
):
    if status is not None and status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status filter")

    repo = AdminBookingRepository(db)
    return repo.list_all_bookings(status=status)
