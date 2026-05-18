import pytest


BASE_URL = "/api/v1/organizations/"
NON_EXISTENT_ID = 99999

ORG_PAYLOAD = {
    "name": "Acme Corp",
    "description": "A test organization",
    "status": "active",
}


@pytest.fixture()
def created_org(client):
    response = client.post(BASE_URL, json=ORG_PAYLOAD)
    return response.json()["data"]


# ── CREATE ────────────────────────────────────────────────────────────────────


def test_create_organization(client):
    response = client.post(BASE_URL, json=ORG_PAYLOAD)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == ORG_PAYLOAD["name"]
    assert data["description"] == ORG_PAYLOAD["description"]
    assert data["status"] == ORG_PAYLOAD["status"]
    assert "id" in data


def test_create_organization_without_optional_fields(client):
    response = client.post(BASE_URL, json={"name": "Minimal Org"})

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Minimal Org"
    assert data["description"] is None
    assert data["status"] == "active"


def test_create_organization_missing_required_fields(client):
    response = client.post(BASE_URL, json={})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": ""},
        {"name": "A" * 101},
        {"description": "D" * 256},
        {"status": "invalid_status"},
    ],
    ids=["empty_name", "name_too_long", "description_too_long", "invalid_status"],
)
def test_create_organization_invalid_payload(client, overrides):
    payload = {**ORG_PAYLOAD, **overrides}
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 422


# ── LIST ──────────────────────────────────────────────────────────────────────


def test_list_organizations_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0


def test_list_organizations_returns_created_organizations(client, created_org):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["id"] == created_org["id"]


def test_list_organizations_pagination(client):
    for i in range(3):
        client.post(BASE_URL, json={**ORG_PAYLOAD, "name": f"Org {i}"})

    response = client.get(BASE_URL, params={"page": 1, "page_size": 2})

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 2
    assert body["meta"]["total"] == 3
    assert body["meta"]["total_pages"] == 2


def test_list_organizations_invalid_pagination(client):
    response = client.get(BASE_URL, params={"page": 0})

    assert response.status_code == 422


# ── GET BY ID ─────────────────────────────────────────────────────────────────


def test_get_organization_by_id(client, created_org):
    response = client.get(f"{BASE_URL}{created_org['id']}")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == created_org["id"]
    assert data["name"] == created_org["name"]


def test_get_organization_not_found(client):
    response = client.get(f"{BASE_URL}{NON_EXISTENT_ID}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"


# ── UPDATE (PUT) ──────────────────────────────────────────────────────────────


def test_update_organization(client, created_org):
    update_payload = {
        "name": "Updated Corp",
        "description": "Updated description",
        "status": "inactive",
    }
    response = client.put(f"{BASE_URL}{created_org['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Updated Corp"
    assert data["description"] == "Updated description"
    assert data["status"] == "inactive"


def test_update_organization_not_found(client):
    response = client.put(
        f"{BASE_URL}{NON_EXISTENT_ID}",
        json={"name": "Updated Corp", "status": "active"},
    )

    assert response.status_code == 404


def test_update_organization_invalid_status(client, created_org):
    response = client.put(
        f"{BASE_URL}{created_org['id']}",
        json={"name": "Updated Corp", "status": "deleted"},
    )

    assert response.status_code == 422


# ── PARTIAL UPDATE (PATCH) ────────────────────────────────────────────────────


def test_partial_update_organization(client, created_org):
    response = client.patch(
        f"{BASE_URL}{created_org['id']}",
        json={"name": "Patched Corp"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Patched Corp"
    assert data["description"] == created_org["description"]
    assert data["status"] == created_org["status"]


def test_partial_update_organization_not_found(client):
    response = client.patch(
        f"{BASE_URL}{NON_EXISTENT_ID}",
        json={"name": "Patched Corp"},
    )

    assert response.status_code == 404


def test_partial_update_organization_invalid_status(client, created_org):
    response = client.patch(
        f"{BASE_URL}{created_org['id']}",
        json={"status": "deleted"},
    )

    assert response.status_code == 422


# ── DELETE ────────────────────────────────────────────────────────────────────


def test_delete_organization(client, created_org):
    response = client.delete(f"{BASE_URL}{created_org['id']}")

    assert response.status_code == 204


def test_delete_organization_makes_organization_unreachable(client, created_org):
    client.delete(f"{BASE_URL}{created_org['id']}")
    response = client.get(f"{BASE_URL}{created_org['id']}")

    assert response.status_code == 404


def test_delete_organization_not_found(client):
    response = client.delete(f"{BASE_URL}{NON_EXISTENT_ID}")

    assert response.status_code == 404
