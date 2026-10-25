from app.errors import DuplicateEmailError, InvalidCredentialsError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.security import create_access_token, hash_password, verify_password


class AuthService:
    """Registration and login use-cases."""

    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def register(self, email: str, password: str) -> User:
        email = email.strip().lower()
        if self.users.get_by_email(email) is not None:
            raise DuplicateEmailError()
        return self.users.add(email=email, password_hash=hash_password(password))

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email.strip().lower())
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_access_token(user)
