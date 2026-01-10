from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password

class UnauthorizedError(Exception):
    pass

class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def authenticate(self, email: str, password: str) -> User:
        user = self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if user is None:
            raise UnauthorizedError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")

        return user
