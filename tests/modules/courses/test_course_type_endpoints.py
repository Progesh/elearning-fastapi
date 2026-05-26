
BASE_URL = "/api/v1/course_types/"

COURSE_TYPE_PAYLOAD = {
    "name": "Math",
    "status": "active",
}


def test_create_course_type(client):
    response = client.post(BASE_URL, json=COURSE_TYPE_PAYLOAD)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Math"
    assert data["status"] == "active"


def test_create_coures_type_missing_required_fields(client):
    response = client.post(BASE_URL, json={})

    assert response.status_code == 422


def test_get_course_types(client):
    # Create a course type
    client.post(BASE_URL, json=COURSE_TYPE_PAYLOAD)
    # List course types
    response = client.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()["data"]
    assert any(item["name"] == "Math" for item in data)


def test_get_course_type_by_id(client):
    # Create a course type
    resp = client.post(BASE_URL, json=COURSE_TYPE_PAYLOAD)
    course_type_id = resp.json()["data"]["id"]
    # Get by id
    response = client.get(f"{BASE_URL}{course_type_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == course_type_id
    assert data["name"] == "Math"


def test_update_course_type(client):
    # Create a course type
    resp = client.post(BASE_URL, json=COURSE_TYPE_PAYLOAD)
    course_type_id = resp.json()["data"]["id"]
    # Update
    update_payload = {"name": "Science", "status": "inactive"}
    response = client.put(f"{BASE_URL}{course_type_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Science"
    assert data["status"] == "inactive"


def test_delete_course_type(client):
    # Create a course type
    resp = client.post(BASE_URL, json=COURSE_TYPE_PAYLOAD)
    course_type_id = resp.json()["data"]["id"]
    # Delete
    response = client.delete(f"{BASE_URL}{course_type_id}")
    assert response.status_code == 204
    # Confirm deleted (should 404 or not found)
    get_resp = client.get(f"{BASE_URL}{course_type_id}")
    assert get_resp.status_code == 404


def test_get_nonexistent_course_type(client):
    response = client.get(f"{BASE_URL}99999")
    assert response.status_code == 404


def test_update_nonexistent_course_type(client):
    response = client.put(f"{BASE_URL}99999", json=COURSE_TYPE_PAYLOAD)
    assert response.status_code == 404


def test_delete_nonexistent_course_type(client):
    response = client.delete(f"{BASE_URL}99999")
    assert response.status_code == 404
