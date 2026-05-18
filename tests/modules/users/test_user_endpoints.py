import pytest


BASE_URL = "/api/v1/users/"
NON_EXISTENT_ID = 99999

USER_PAYLOAD = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1111111111",
    "status": "active",
}


@pytest.fixture()
def created_user(client):
    response = client.post(BASE_URL, json=USER_PAYLOAD)
    return response.json()["data"]


# ── CREATE ────────────────────────────────────────────────────────────────────


def test_create_user(client):
    response = client.post(BASE_URL, json=USER_PAYLOAD)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["email"] == USER_PAYLOAD["email"]
    assert data["first_name"] == USER_PAYLOAD["first_name"]
    assert data["last_name"] == USER_PAYLOAD["last_name"]
    assert data["phone"] == USER_PAYLOAD["phone"]
    assert data["status"] == USER_PAYLOAD["status"]
    assert "id" in data


def test_create_user_duplicate_email(client):
    client.post(BASE_URL, json=USER_PAYLOAD)
    response = client.post(BASE_URL, json=USER_PAYLOAD)

    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"


def test_create_user_missing_required_fields(client):
    response = client.post(BASE_URL, json={})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "overrides",
    [
        {"email": "not-an-email"},
        {"status": "invalid_status"},
        {"first_name": "J" * 101},
        {"first_name": ""},
    ],
    ids=["invalid_email", "invalid_status", "first_name_too_long", "empty_first_name"],
)
def test_create_user_invalid_payload(client, overrides):
    payload = {**USER_PAYLOAD, **overrides}
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 422


# ── LIST ──────────────────────────────────────────────────────────────────────


def test_list_users_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0


def test_list_users_returns_created_users(client, created_user):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["id"] == created_user["id"]


def test_list_users_pagination(client):
    for i in range(3):
        client.post(BASE_URL, json={**USER_PAYLOAD, "email": f"user{i}@example.com"})

    response = client.get(BASE_URL, params={"page": 1, "page_size": 2})

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 2
    assert body["meta"]["total"] == 3
    assert body["meta"]["total_pages"] == 2


def test_list_users_invalid_pagination(client):
    response = client.get(BASE_URL, params={"page": 0})

    assert response.status_code == 422


# ── GET BY ID ─────────────────────────────────────────────────────────────────


def test_get_user_by_id(client, created_user):
    response = client.get(f"{BASE_URL}{created_user['id']}")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == created_user["id"]
    assert data["email"] == created_user["email"]


def test_get_user_not_found(client):
    response = client.get(f"{BASE_URL}{NON_EXISTENT_ID}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# ── UPDATE (PUT) ──────────────────────────────────────────────────────────────


def test_update_user(client, created_user):
    update_payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "2222222222",
        "status": "inactive",
    }
    response = client.put(f"{BASE_URL}{created_user['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["phone"] == "2222222222"
    assert data["status"] == "inactive"


def test_update_user_not_found(client):
    response = client.put(
        f"{BASE_URL}{NON_EXISTENT_ID}",
        json={"first_name": "Jane", "last_name": "Smith", "status": "active"},
    )

    assert response.status_code == 404


def test_update_user_invalid_status(client, created_user):
    response = client.put(
        f"{BASE_URL}{created_user['id']}",
        json={"first_name": "Jane", "last_name": "Smith", "status": "deleted"},
    )

    assert response.status_code == 422


# ── PARTIAL UPDATE (PATCH) ────────────────────────────────────────────────────


def test_partial_update_user(client, created_user):
    response = client.patch(
        f"{BASE_URL}{created_user['id']}",
        json={"first_name": "Jane"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["first_name"] == "Jane"
    assert data["last_name"] == created_user["last_name"]


def test_partial_update_user_not_found(client):
    response = client.patch(f"{BASE_URL}{NON_EXISTENT_ID}", json={"first_name": "Jane"})

    assert response.status_code == 404


def test_partial_update_user_invalid_status(client, created_user):
    response = client.patch(
        f"{BASE_URL}{created_user['id']}",
        json={"status": "deleted"},
    )

    assert response.status_code == 422


# ── DELETE ────────────────────────────────────────────────────────────────────


def test_delete_user(client, created_user):
    response = client.delete(f"{BASE_URL}{created_user['id']}")

    assert response.status_code == 204


def test_delete_user_makes_user_unreachable(client, created_user):
    client.delete(f"{BASE_URL}{created_user['id']}")
    response = client.get(f"{BASE_URL}{created_user['id']}")

    assert response.status_code == 404


def test_delete_user_not_found(client):
    response = client.delete(f"{BASE_URL}{NON_EXISTENT_ID}")

    assert response.status_code == 404
