import pytest
from fastapi.testclient import TestClient
from rest_api.main import app

client = TestClient(app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Financial Data API"}
