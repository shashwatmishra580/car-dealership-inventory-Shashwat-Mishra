"""Application settings, overridable through environment variables."""
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me-in-production-0123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dealership.db")
