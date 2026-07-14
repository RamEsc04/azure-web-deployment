import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIRECTORY = PROJECT_ROOT / "app"

sys.path.insert(0, str(APP_DIRECTORY))

from app import app


def test_home_route():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Aplicaci" in response.data


def test_health_route():
    client = app.test_client()

    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["environment"] == "dev"