import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.api import myapp
from src.database import get_db

client = TestClient(myapp)


@pytest.fixture
def api_client():
    return client


@pytest.fixture
def mock_db():
    db = AsyncMock()
    myapp.dependency_overrides[get_db] = lambda: db
    yield db
    myapp.dependency_overrides.clear()


@pytest.mark.parametrize("currency,expected_status", [
    ("USD", 200),
    ("EUR", 200),
    ("GBP", 404),
    ("JPY", 404),
])
def test_get_rate(api_client, currency, expected_status):
    response = api_client.get(f"/rates/{currency}")
    assert response.status_code == expected_status


@pytest.mark.parametrize("currency,limit", [
    ("USD", 10),
    ("EUR", 5),
    ("GBP", 1),
])
def test_get_history(api_client, currency, limit):
    response = api_client.get(f"/history?currency={currency}&limit={limit}")
    assert response.status_code == 200
    assert response.json() == {"currency": currency, "limit": limit}


def test_get_rate_not_found(api_client):
    response = api_client.get("/rates/GBP")
    assert response.status_code == 404
    assert response.json() == {"detail": "Валюта не найдена"}


def test_create_rate_db_mocked(api_client, mock_db):
    response = api_client.post("/rates/db", json={"currency": "USD", "rate": 92.5})
    assert response.status_code == 200
    assert response.json()["status"] == "saved to db"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()