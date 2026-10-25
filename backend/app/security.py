"""Password hashing and JWT helpers."""
import base64
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app import config


def _prepare(password: str) -> bytes:
    """Pre-hash so bcrypt's 72-byte input limit never rejects long passphrases."""
    return base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    return bcrypt.hashpw(_prepare(password), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(_prepare(password), password_hash.encode("utf-8"))


def create_access_token(user) -> str:
    """Issue a signed JWT carrying the user's id, email and role."""
    expires = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "email": user.email, "role": user.role, "exp": expires}
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


def decode_token(token: str) -> dict:
    """Validate signature + expiry; raises jwt.PyJWTError on failure."""
    return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
