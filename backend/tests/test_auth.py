import jwt

from app.models import User

CREDS = {"email": "jane@example.com", "password": "Password123"}


def test_register_creates_user(client):
    response = client.post("/api/auth/register", json=CREDS)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == CREDS["email"]
    assert body["role"] == "USER"
    assert "password" not in body and "password_hash" not in body


def test_register_stores_hashed_password(client, session_factory):
    client.post("/api/auth/register", json=CREDS)
    with session_factory() as db:
        user = db.query(User).filter_by(email=CREDS["email"]).one()
    assert user.password_hash != CREDS["password"]
    assert user.password_hash.startswith("$2")


def test_register_duplicate_email_conflicts(client):
    client.post("/api/auth/register", json=CREDS)
    response = client.post("/api/auth/register", json=CREDS)
    assert response.status_code == 409


def test_register_normalizes_email_case(client):
    client.post("/api/auth/register", json={"email": "Mixed@Example.com", "password": "Password123"})
    response = client.post("/api/auth/login", json={"email": "mixed@example.com", "password": "Password123"})
    assert response.status_code == 200


def test_register_rejects_invalid_email(client):
    response = client.post("/api/auth/register", json={"email": "not-an-email", "password": "Password123"})
    assert response.status_code == 422


def test_register_rejects_short_password(client):
    response = client.post("/api/auth/register", json={"email": "a@example.com", "password": "short"})
    assert response.status_code == 422


def test_login_returns_jwt_with_role(client):
    client.post("/api/auth/register", json=CREDS)
    response = client.post("/api/auth/login", json=CREDS)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    claims = jwt.decode(body["access_token"], options={"verify_signature": False})
    assert claims["role"] == "USER"
    assert claims["email"] == CREDS["email"]


def test_login_wrong_password_is_unauthorized(client):
    client.post("/api/auth/register", json=CREDS)
    response = client.post("/api/auth/login", json={**CREDS, "password": "WrongPassword1"})
    assert response.status_code == 401


def test_login_unknown_user_is_unauthorized(client):
    response = client.post("/api/auth/login", json=CREDS)
    assert response.status_code == 401
