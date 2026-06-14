"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_companies():
    response = client.get("/api/companies")
    assert response.status_code == 200
    data = response.json()
    assert "companies" in data
    assert isinstance(data["companies"], list)


def test_search():
    response = client.post("/api/search", json={
        "question": "risk factors",
    })
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
