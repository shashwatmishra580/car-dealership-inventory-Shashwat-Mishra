import pytest

FLEET = [
    {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 5},
    {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 32000, "quantity": 3},
    {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24000, "quantity": 0},
    {"make": "Ford", "model": "F-150", "category": "Truck", "price": 45000, "quantity": 2},
]


@pytest.fixture()
def fleet(client, admin_headers):
    for car in FLEET:
        client.post("/api/vehicles", json=car, headers=admin_headers)


def search(client, headers, **params):
    response = client.get("/api/vehicles/search", params=params, headers=headers)
    assert response.status_code == 200, response.text
    return sorted(v["model"] for v in response.json())


def test_search_requires_authentication(client):
    assert client.get("/api/vehicles/search").status_code == 401


def test_search_without_filters_returns_everything(client, user_headers, fleet):
    assert search(client, user_headers) == ["Camry", "Civic", "F-150", "RAV4"]


def test_search_by_make_is_case_insensitive(client, user_headers, fleet):
    assert search(client, user_headers, make="toyota") == ["Camry", "RAV4"]


def test_search_by_partial_model(client, user_headers, fleet):
    assert search(client, user_headers, model="ra") == ["RAV4"]


def test_search_by_category(client, user_headers, fleet):
    assert search(client, user_headers, category="sedan") == ["Camry", "Civic"]


def test_search_by_min_price(client, user_headers, fleet):
    assert search(client, user_headers, min_price=30000) == ["F-150", "RAV4"]


def test_search_by_max_price(client, user_headers, fleet):
    assert search(client, user_headers, max_price=25000) == ["Civic"]


def test_search_by_price_range(client, user_headers, fleet):
    assert search(client, user_headers, min_price=25000, max_price=33000) == ["Camry", "RAV4"]


def test_search_combines_filters(client, user_headers, fleet):
    assert search(client, user_headers, make="Toyota", category="Sedan") == ["Camry"]


def test_search_with_no_matches_returns_empty_list(client, user_headers, fleet):
    assert search(client, user_headers, make="Tesla") == []


def test_search_rejects_inverted_price_range(client, user_headers, fleet):
    response = client.get("/api/vehicles/search", params={"min_price": 50000, "max_price": 100}, headers=user_headers)
    assert response.status_code == 400
