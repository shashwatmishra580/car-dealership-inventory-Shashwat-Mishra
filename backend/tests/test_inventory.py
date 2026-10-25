import pytest


def make_vehicle(client, headers, quantity):
    payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24000, "quantity": quantity}
    return client.post("/api/vehicles", json=payload, headers=headers).json()


def stock_of(client, headers, vehicle_id):
    vehicles = client.get("/api/vehicles", headers=headers).json()
    return next(v["quantity"] for v in vehicles if v["id"] == vehicle_id)


# ---------------------------------------------------------------- purchase
def test_purchase_requires_authentication(client, sample_vehicle):
    assert client.post(f"/api/vehicles/{sample_vehicle['id']}/purchase").status_code == 401


def test_purchase_decrements_quantity_by_one(client, user_headers, sample_vehicle):
    response = client.post(f"/api/vehicles/{sample_vehicle['id']}/purchase", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["quantity"] == 4


def test_purchase_multiple_units(client, user_headers, sample_vehicle):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/purchase", json={"quantity": 3}, headers=user_headers
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 2


def test_purchase_fails_when_out_of_stock(client, user_headers, admin_headers):
    vehicle = make_vehicle(client, admin_headers, quantity=0)
    response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user_headers)
    assert response.status_code == 409
    assert stock_of(client, user_headers, vehicle["id"]) == 0


def test_purchase_more_than_available_leaves_stock_untouched(client, user_headers, sample_vehicle):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/purchase", json={"quantity": 6}, headers=user_headers
    )
    assert response.status_code == 409
    assert stock_of(client, user_headers, sample_vehicle["id"]) == 5


def test_last_unit_cannot_be_bought_twice(client, user_headers, admin_headers):
    vehicle = make_vehicle(client, admin_headers, quantity=1)
    first = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user_headers)
    second = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user_headers)
    assert (first.status_code, second.status_code) == (200, 409)


def test_purchase_unknown_vehicle_returns_404(client, user_headers):
    assert client.post("/api/vehicles/999/purchase", headers=user_headers).status_code == 404


@pytest.mark.parametrize("quantity", [0, -2])
def test_purchase_rejects_non_positive_quantity(client, user_headers, sample_vehicle, quantity):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/purchase", json={"quantity": quantity}, headers=user_headers
    )
    assert response.status_code == 422


# ----------------------------------------------------------------- restock
def test_restock_requires_authentication(client, sample_vehicle):
    response = client.post(f"/api/vehicles/{sample_vehicle['id']}/restock", json={"amount": 5})
    assert response.status_code == 401


def test_restock_is_forbidden_for_regular_users(client, user_headers, sample_vehicle):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/restock", json={"amount": 5}, headers=user_headers
    )
    assert response.status_code == 403


def test_admin_can_restock(client, admin_headers, sample_vehicle):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/restock", json={"amount": 10}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 15


@pytest.mark.parametrize("amount", [0, -3])
def test_restock_rejects_non_positive_amount(client, admin_headers, sample_vehicle, amount):
    response = client.post(
        f"/api/vehicles/{sample_vehicle['id']}/restock", json={"amount": amount}, headers=admin_headers
    )
    assert response.status_code == 422


def test_restock_unknown_vehicle_returns_404(client, admin_headers):
    assert client.post("/api/vehicles/999/restock", json={"amount": 5}, headers=admin_headers).status_code == 404
