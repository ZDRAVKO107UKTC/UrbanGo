from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import JWT_SECRET, JWT_ALG
from app.models.token_blacklist import TokenBlacklist

bearer = HTTPBearer(auto_error=False)

def require_role(required_role: str):
    def _dep(
        creds: HTTPAuthorizationCredentials | None = Depends(bearer),
        db: Session = Depends(get_db),
    ) -> int:
        if creds is None:
            raise HTTPException(status_code=401, detail="Missing token")

        token = creds.credentials

        blacklisted = db.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        ).scalar_one_or_none()

        if blacklisted is not None:
            raise HTTPException(status_code=401, detail="Token revoked")

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")

        return int(payload["sub"])
    return _dep

