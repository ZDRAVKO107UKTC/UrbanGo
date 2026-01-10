from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.repositories.auth_repo import AuthRepository, UnauthorizedError
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    try:
        user = repo.authenticate(email=payload.email, password=payload.password)
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id, role=user.role)
    return TokenResponse(access_token=token)
