import pytest

VEHICLE = {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 5}


def test_vehicles_require_authentication(client):
    assert client.get("/api/vehicles").status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get("/api/vehicles", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_create_vehicle(client, user_headers):
    response = client.post("/api/vehicles", json=VEHICLE, headers=user_headers)
    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert {key: body[key] for key in VEHICLE} == VEHICLE


@pytest.mark.parametrize(
    "field,value",
    [("price", 0), ("price", -1), ("quantity", -1), ("make", ""), ("model", "   ")],
)
def test_create_vehicle_rejects_invalid_values(client, user_headers, field, value):
    response = client.post("/api/vehicles", json={**VEHICLE, field: value}, headers=user_headers)
    assert response.status_code == 422


def test_create_vehicle_requires_all_fields(client, user_headers):
    payload = {key: value for key, value in VEHICLE.items() if key != "model"}
    assert client.post("/api/vehicles", json=payload, headers=user_headers).status_code == 422


def test_list_vehicles_empty(client, user_headers):
    response = client.get("/api/vehicles", headers=user_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_vehicles_returns_all(client, user_headers, sample_vehicle):
    response = client.get("/api/vehicles", headers=user_headers)
    assert response.status_code == 200
    assert [v["id"] for v in response.json()] == [sample_vehicle["id"]]


def test_update_vehicle(client, user_headers, sample_vehicle):
    response = client.put(
        f"/api/vehicles/{sample_vehicle['id']}", json={"price": 26500, "quantity": 9}, headers=user_headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 26500
    assert body["quantity"] == 9
    assert body["make"] == "Toyota"  # untouched fields are preserved


def test_update_unknown_vehicle_returns_404(client, user_headers):
    assert client.put("/api/vehicles/999", json={"price": 100}, headers=user_headers).status_code == 404


def test_update_rejects_invalid_values(client, user_headers, sample_vehicle):
    response = client.put(f"/api/vehicles/{sample_vehicle['id']}", json={"price": -5}, headers=user_headers)
    assert response.status_code == 422


def test_delete_is_forbidden_for_regular_users(client, user_headers, sample_vehicle):
    response = client.delete(f"/api/vehicles/{sample_vehicle['id']}", headers=user_headers)
    assert response.status_code == 403


def test_admin_can_delete_vehicle(client, admin_headers, sample_vehicle):
    response = client.delete(f"/api/vehicles/{sample_vehicle['id']}", headers=admin_headers)
    assert response.status_code == 204
    assert client.get("/api/vehicles", headers=admin_headers).json() == []


def test_delete_unknown_vehicle_returns_404(client, admin_headers):
    assert client.delete("/api/vehicles/999", headers=admin_headers).status_code == 404
