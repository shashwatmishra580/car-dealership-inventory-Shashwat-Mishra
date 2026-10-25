from app.errors import DuplicateEmailError, InvalidCredentialsError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.security import create_access_token, hash_password, verify_password


class AuthService:
    """Registration and login use-cases."""

    def __init__(self, users: UserRepository) -> None:
        self.users = users

    @staticmethod
    def _normalize_email(email: str) -> str:
        """Emails are case-insensitive: store and look them up trimmed and lower-cased."""
        return email.strip().lower()

    def register(self, email: str, password: str) -> User:
        email = self._normalize_email(email)
        if self.users.get_by_email(email) is not None:
            raise DuplicateEmailError()
        return self.users.add(email=email, password_hash=hash_password(password))

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(self._normalize_email(email))
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_access_token(user)
