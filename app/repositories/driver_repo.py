from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class NotFoundError(Exception):
    pass

class BadRequestError(Exception):
    pass

class DriverRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def set_availability(self, driver_id: int, available: bool) -> User:
        with self.db.begin():
            user = self.db.execute(
                select(User).where(User.id == driver_id)
            ).scalar_one_or_none()

            if user is None:
                raise NotFoundError("Driver not found")

            if user.role != "DRIVER":
                raise BadRequestError("User is not a driver")

            user.driver_available = available
            self.db.flush()
            return user
