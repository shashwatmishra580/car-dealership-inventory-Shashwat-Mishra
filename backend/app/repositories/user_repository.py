from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """Data access for users."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def add(self, email: str, password_hash: str, role: str = "USER") -> User:
        user = User(email=email, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
