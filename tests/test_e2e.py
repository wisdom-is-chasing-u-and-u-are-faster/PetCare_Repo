import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_e2e_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_health_check_endpoint():
    """Verify system health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "enterprise-digital-banking"


def test_dashboard_summary():
    """Verify aggregated dashboard summary endpoint."""
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_balance"] > 0
    assert data["total_accounts"] >= 3
    assert data["active_cards"] >= 1
    assert "recent_transactions" in data


def test_static_index_mount():
    """Verify static index HTML page is served at root."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Digital Banking Portal" in response.text
