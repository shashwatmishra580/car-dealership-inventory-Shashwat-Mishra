import os

os.environ["BCRYPT_ROUNDS"] = "4"  # keep password hashing fast in tests

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db, make_engine
from app.main import app
from app.models import User
from app.security import hash_password

ADMIN_EMAIL, ADMIN_PASSWORD = "admin@example.com", "Admin12345"
USER_EMAIL, USER_PASSWORD = "user@example.com", "Password123"


@pytest.fixture()
def session_factory(tmp_path):
    """A fresh on-disk SQLite database for every test (never in-memory)."""
    engine = make_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False)
    engine.dispose()


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _login(client, email, password):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture()
def user_headers(client):
    client.post("/api/auth/register", json={"email": USER_EMAIL, "password": USER_PASSWORD})
    return _login(client, USER_EMAIL, USER_PASSWORD)


@pytest.fixture()
def admin_headers(client, session_factory):
    with session_factory() as db:
        db.add(User(email=ADMIN_EMAIL, password_hash=hash_password(ADMIN_PASSWORD), role="ADMIN"))
        db.commit()
    return _login(client, ADMIN_EMAIL, ADMIN_PASSWORD)


@pytest.fixture()
def sample_vehicle(client, admin_headers):
    payload = {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 5}
    return client.post("/api/vehicles", json=payload, headers=admin_headers).json()
