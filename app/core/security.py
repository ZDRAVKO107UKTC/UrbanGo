from __future__ import annotations

import hashlib
import bcrypt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "CHANGE_ME"
JWT_ALG = "HS256"
JWT_EXPIRES_MIN = 60

def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")

    sha = hashlib.sha256(pw_bytes).digest()

    hashed = bcrypt.hashpw(sha, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    sha = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.checkpw(sha, hashed.encode("utf-8"))

def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRES_MIN)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
