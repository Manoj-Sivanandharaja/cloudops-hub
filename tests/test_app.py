import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

# The application reads these variables when it is imported.
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")

from app import app


def setup_function():
    app.config["TESTING"] = True


def make_task(task_id=1):
    now = datetime.now(timezone.utc)
    return {
        "id": task_id,
        "title": "Test task",
        "description": "Created by automated test",
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }


def mock_database():
    connection_context = MagicMock()
    connection = connection_context.__enter__.return_value
    return connection_context, connection


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_health_endpoint_when_database_is_connected():
    client = app.test_client()
    context, connection = mock_database()

    with patch("app.get_db", return_value=context):
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["database"] == "connected"
    connection.execute.assert_called_once_with("SELECT 1")


def test_list_tasks():
    client = app.test_client()
    context, connection = mock_database()
    connection.execute.return_value.fetchall.return_value = [make_task()]

    with patch("app.get_db", return_value=context):
        response = client.get("/api/tasks")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Test task"


def test_create_task():
    client = app.test_client()
    context, connection = mock_database()
    connection.execute.return_value.fetchone.return_value = make_task()

    with patch("app.get_db", return_value=context):
        response = client.post(
            "/api/tasks",
            json={
                "title": "Test task",
                "description": "Created by automated test",
            },
        )

    assert response.status_code == 201
    assert response.json["title"] == "Test task"
    assert response.json["status"] == "pending"


def test_create_task_rejects_empty_title():
    client = app.test_client()

    response = client.post("/api/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert "error" in response.json


def test_create_task_rejects_invalid_status():
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={"title": "Test task", "status": "invalid"},
    )

    assert response.status_code == 400
    assert "error" in response.json


def test_get_task_not_found():
    client = app.test_client()
    context, connection = mock_database()
    connection.execute.return_value.fetchone.return_value = None

    with patch("app.get_db", return_value=context):
        response = client.get("/api/tasks/999")

    assert response.status_code == 404
    assert response.json["error"] == "Task not found"


def test_update_task_not_found():
    client = app.test_client()
    context, connection = mock_database()
    connection.execute.return_value.fetchone.return_value = None

    with patch("app.get_db", return_value=context):
        response = client.put(
            "/api/tasks/999",
            json={"title": "Updated task"},
        )

    assert response.status_code == 404
    assert response.json["error"] == "Task not found"


def test_delete_task_not_found():
    client = app.test_client()
    context, connection = mock_database()
    connection.execute.return_value.fetchone.return_value = None

    with patch("app.get_db", return_value=context):
        response = client.delete("/api/tasks/999")

    assert response.status_code == 404
    assert response.json["error"] == "Task not found"
