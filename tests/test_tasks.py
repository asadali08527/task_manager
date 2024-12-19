from tests.conftest import client

test_client = client


def test_create_task():
    response = test_client.post(
        "/tasks", json={"title": "Test Task",
                        "description": "Test Description"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

    # Negative scenario - Missing title
    response = test_client.post(
        "/tasks", json={"description": "Test Description"})
    assert response.status_code == 422  # Unprocessable Entity


def test_get_tasks():
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id():
    response = test_client.post("/tasks", json={"title": "Test Task"})
    task_id = response.json()["id"]
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # Negative scenario - Invalid ID
    invalid_id = 10001
    response = test_client.get(f"/tasks/{invalid_id}")
    assert response.status_code == 404  # Not Found


def test_update_task():
    response = test_client.post("/tasks", json={"title": "Test Task"})
    task_id = response.json()["id"]
    response = test_client.put(
        f"/tasks/{task_id}", json={"title": "Updated Task"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

    # Negative scenario - Invalid ID
    invalid_id = 10001
    response = test_client.put(
        f"/tasks/{invalid_id}", json={"title": "Updated Task"})
    assert response.status_code == 404  # Not Found


def test_delete_task():
    response = test_client.post("/tasks", json={"title": "Task to Delete"})
    task_id = response.json()["id"]
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {
        "detail": f"Task:{task_id} deleted successfully"}

    # Negative scenario - Invalid ID
    invalid_id = 10001
    response = test_client.delete(f"/tasks/{invalid_id}")
    assert response.status_code == 404  # Not Found


def test_get_tasks_by_completed_status():
    # Positive scenario - Filtering tasks by completed status
    test_client.post("/tasks", json={"title": "Task 1", "completed": True})
    test_client.post("/tasks", json={"title": "Task 2", "completed": False})

    response = test_client.get("/tasks?completed=true")
    assert response.status_code == 200
    assert all(task["completed"] is True for task in response.json())

    response = test_client.get("/tasks?completed=false")
    assert response.status_code == 200
    assert all(task["completed"] is False for task in response.json())


def test_patch_task():
    # Positive scenario - Updating completed status
    response = test_client.post("/tasks", json={"title": "Task to Patch"})
    task_id = response.json()["id"]
    response = test_client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Negative scenario - Invalid ID
    invalid_id = 10001
    response = test_client.patch(
        f"/tasks/{invalid_id}", json={"completed": True})
    assert response.status_code == 404  # Not Found


def test_empty_title_post():
    response = test_client.post(
        "/tasks", json={"title": "  ", "description": "Description"}
    )
    assert response.status_code == 400
    assert response.json()[
        "detail"] == "Title is required and cannot be empty."


def test_empty_patch_update():
    response = test_client.post("/tasks", json={"title": "Task to Patch"})
    task_id = response.json()["id"]
    response = test_client.patch(f"/tasks/{task_id}", json={})
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "At least one of 'title', 'description',"
        " or 'completed' must be provided."
    )
