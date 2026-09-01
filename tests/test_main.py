"""Sanity checks for the API surface."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_hello_world() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_hello_endpoint_returns_hello_world() -> None:
    response = client.get("/api/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_health_endpoint_reports_ok() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
