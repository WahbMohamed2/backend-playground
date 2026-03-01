import pytest

def test_create_task(client, auth_headers):
    response = client.post("/tasks/", json={
        "title": "My first task",
        "priority": "high"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first task"
    assert data["priority"] == "high"
    assert data["status"] == "todo"

def test_create_task_blank_title(client, auth_headers):
    response = client.post("/tasks/", json={
        "title": "   ",
        "priority": "high"
    }, headers=auth_headers)
    # Why 422: Pydantic validator rejects blank titles
    assert response.status_code == 422

def test_create_task_invalid_priority(client, auth_headers):
    response = client.post("/tasks/", json={
        "title": "Valid title",
        "priority": "urgent"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_get_tasks(client, auth_headers):
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tasks_unauthenticated(client):
    response = client.get("/tasks/")
    # Why 401: no token means no access
    assert response.status_code == 401

def test_update_task(client, auth_headers):
    # Create a task first
    create = client.post("/tasks/", json={"title": "To update"}, headers=auth_headers)
    task_id = create.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "status": "in_progress"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    # Why check title: exclude_unset means title should be unchanged
    assert response.json()["title"] == "To update"

def test_delete_task(client, auth_headers):
    create = client.post("/tasks/", json={"title": "To delete"}, headers=auth_headers)
    task_id = create.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Confirm it's gone
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404

def test_get_tasks_filter_by_priority(client, auth_headers):
    client.post("/tasks/", json={"title": "Low task", "priority": "low"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "High task", "priority": "high"}, headers=auth_headers)

    response = client.get("/tasks/?priority=low", headers=auth_headers)
    assert response.status_code == 200
    for task in response.json():
        assert task["priority"] == "low"
