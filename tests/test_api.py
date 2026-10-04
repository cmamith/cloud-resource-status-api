from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_get_existing_instance():
    response = client.get("/instances/i-001")

    assert response.status_code == 200
    assert response.json()["instance_id"] == "i-001"
    assert response.json()["state"] == "running"


def test_get_missing_instance():
    response = client.get("/instances/i-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Instance not found"
    }