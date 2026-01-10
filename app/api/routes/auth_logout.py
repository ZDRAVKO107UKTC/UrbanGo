from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt

from app.core.db import get_db
from app.core.security import JWT_SECRET, JWT_ALG
from app.models.token_blacklist import TokenBlacklist
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer(auto_error=True)

@router.post("/logout", status_code=204)
def logout(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    token = creds.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    db.add(TokenBlacklist(token=token, expires_at=expires_at))
    db.commit()

    return None
