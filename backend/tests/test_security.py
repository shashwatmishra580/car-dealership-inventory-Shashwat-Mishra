import jwt
import pytest

from app import config
from app.security import create_access_token, decode_token, hash_password, verify_password


class FakeUser:
    id = 7
    email = "x@example.com"
    role = "ADMIN"


def test_hashes_are_salted_and_verifiable():
    first, second = hash_password("Password123"), hash_password("Password123")
    assert first != second
    assert verify_password("Password123", first)
    assert not verify_password("wrong-password", first)


def test_very_long_passwords_are_supported():
    long_password = "x" * 200
    assert verify_password(long_password, hash_password(long_password))


def test_token_round_trip():
    claims = decode_token(create_access_token(FakeUser()))
    assert claims["sub"] == "7"
    assert claims["role"] == "ADMIN"


def test_expired_token_is_rejected(monkeypatch):
    monkeypatch.setattr(config, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(create_access_token(FakeUser()))
