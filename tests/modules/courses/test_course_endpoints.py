import pytest

COURSE_BASE_URL = "/api/v1/courses/"
COURSE_TYPE_BASE_URL = "/api/v1/course_types/"

ACTIVE_COURSE_TYPE_PAYLOAD = {
    "name": "Active Type",
    "status": "active",
}


@pytest.fixture()
def active_course_type(client):
    response = client.post(COURSE_TYPE_BASE_URL, json=ACTIVE_COURSE_TYPE_PAYLOAD)
    assert response.status_code == 201
    return response.json()["data"]


@pytest.fixture()
def inactive_course_type(client):
    response = client.post(
        COURSE_TYPE_BASE_URL, json={"name": "Inactive Type", "status": "active"}
    )
    assert response.status_code == 201

    course_type_id = response.json()["data"]["id"]
    deactivate_response = client.put(
        f"{COURSE_TYPE_BASE_URL}{course_type_id}",
        json={"name": "Inactive Type", "status": "inactive"},
    )
    assert deactivate_response.status_code == 200

    return deactivate_response.json()["data"]


@pytest.fixture()
def deleted_course_type(client):
    response = client.post(
        COURSE_TYPE_BASE_URL, json={"name": "Deleted Type", "status": "active"}
    )
    assert response.status_code == 201

    course_type_id = response.json()["data"]["id"]
    delete_response = client.delete(f"{COURSE_TYPE_BASE_URL}{course_type_id}")
    assert delete_response.status_code == 204

    return {"id": course_type_id}


@pytest.fixture()
def created_course(client, active_course_type):
    payload = {
        "name": "Core Course",
        "description": "Core description",
        "status": "active",
        "course_type_id": active_course_type["id"],
    }

    response = client.post(COURSE_BASE_URL, json=payload)
    assert response.status_code == 201

    return response.json()["data"]


def test_create_course_with_active_course_type(client, active_course_type):
    payload = {
        "name": "Algebra 101",
        "description": "Intro to algebra",
        "status": "active",
        "course_type_id": active_course_type["id"],
    }

    response = client.post(COURSE_BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == payload["name"]
    assert data["course_type_id"] == active_course_type["id"]


def test_create_course_with_inactive_course_type_fails(client, inactive_course_type):
    payload = {
        "name": "Physics 101",
        "description": "Intro to physics",
        "status": "active",
        "course_type_id": inactive_course_type["id"],
    }

    response = client.post(COURSE_BASE_URL, json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "course_type_id"]
    assert detail[0]["msg"] == "course_type_id must reference an active course type"


def test_create_course_with_nonexistent_course_type_fails(client):
    payload = {
        "name": "Biology 101",
        "description": "Intro to biology",
        "status": "active",
        "course_type_id": 99999,
    }

    response = client.post(COURSE_BASE_URL, json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "course_type_id"]
    assert detail[0]["msg"] == "course_type_id must reference an active course type"


def test_create_course_with_deleted_course_type_fails(client, deleted_course_type):
    payload = {
        "name": "History 101",
        "description": "Intro to history",
        "status": "active",
        "course_type_id": deleted_course_type["id"],
    }

    response = client.post(COURSE_BASE_URL, json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "course_type_id"]
    assert detail[0]["msg"] == "course_type_id must reference an active course type"


def test_create_course_without_course_type_id_fails(client):
    payload = {
        "name": "Chemistry 101",
        "description": "Intro to chemistry",
        "status": "active",
    }

    response = client.post(COURSE_BASE_URL, json=payload)

    assert response.status_code == 422


def test_get_courses(client, created_course):
    response = client.get(COURSE_BASE_URL)

    assert response.status_code == 200
    data = response.json()["data"]
    assert any(item["id"] == created_course["id"] for item in data)


def test_get_course_by_id(client, created_course):
    response = client.get(f"{COURSE_BASE_URL}{created_course['id']}")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == created_course["id"]


def test_get_nonexistent_course_fails(client):
    response = client.get(f"{COURSE_BASE_URL}99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"


def test_update_course(client, created_course, active_course_type):
    payload = {
        "name": "Updated Course",
        "description": "Updated description",
        "status": "inactive",
        "course_type_id": active_course_type["id"],
    }

    response = client.put(f"{COURSE_BASE_URL}{created_course['id']}", json=payload)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Updated Course"
    assert data["status"] == "inactive"


def test_update_course_with_inactive_course_type_fails(
    client, created_course, inactive_course_type
):
    payload = {
        "name": "Updated Course",
        "description": "Updated description",
        "status": "active",
        "course_type_id": inactive_course_type["id"],
    }

    response = client.put(f"{COURSE_BASE_URL}{created_course['id']}", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "course_type_id"]


def test_update_nonexistent_course_fails(client, active_course_type):
    payload = {
        "name": "Updated Course",
        "description": "Updated description",
        "status": "active",
        "course_type_id": active_course_type["id"],
    }

    response = client.put(f"{COURSE_BASE_URL}99999", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"


def test_delete_course(client, created_course):
    response = client.delete(f"{COURSE_BASE_URL}{created_course['id']}")

    assert response.status_code == 204

    get_response = client.get(f"{COURSE_BASE_URL}{created_course['id']}")
    assert get_response.status_code == 404


def test_delete_nonexistent_course_fails(client):
    response = client.delete(f"{COURSE_BASE_URL}99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"
