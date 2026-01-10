from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.security import JWT_SECRET, JWT_ALG

bearer = HTTPBearer(auto_error=False)

def require_role(required_role: str):
    def _dep(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if creds is None:
            raise HTTPException(status_code=401, detail="Missing token")

        token = creds.credentials
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        role = payload.get("role")
        user_id = payload.get("sub")

        if role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")

        return int(user_id)
    return _dep
