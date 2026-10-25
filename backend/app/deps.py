"""Shared FastAPI dependencies: authentication, authorization, service wiring."""
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.security import decode_token
from app.services.vehicle_service import VehicleService

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the bearer token to a user, or raise 401."""
    unauthorized = HTTPException(
        status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"}
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError:
        raise unauthorized
    user = UserRepository(db).get_by_id(int(payload["sub"]))
    if user is None:
        raise unauthorized
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """Allow only ADMIN users, or raise 403."""
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user


def get_vehicle_service(db: Session = Depends(get_db)) -> VehicleService:
    return VehicleService(VehicleRepository(db))
