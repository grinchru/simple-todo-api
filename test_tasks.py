from fastapi.testclient import TestClient
from main import app, tasks
import pytest

client = TestClient(app)

@pytest.fixture
def sample_task():
    return {"title": "Устанавливать все игры", "description": "кроме платных"}

@pytest.fixture(autouse=True)
def clear_tasks():
    tasks.clear()
    yield
    tasks.clear()

def test_create_task_success(sample_task):
    response = client.post("/tasks", json=sample_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_task["title"]
    assert data["description"] == sample_task["description"]

def test_get_tasks(sample_task):
    response = client.post("/tasks", json=sample_task)
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_task["title"]

@pytest.mark.parametrize("invalid_payload", [{"title": "ой"}, {"title": ""}, {"title": 67},
                                             {"title": "Z" * 101}, {}])
def test_create_task_invalid(invalid_payload):
    response = client.post("/tasks", json=invalid_payload)
    assert response.status_code == 422
    