import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_cards_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_list_cards():
    """Verify retrieval of registered cards."""
    response = client.get("/api/v1/cards")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) >= 2
    assert "card_number_masked" in cards[0]


def test_toggle_card_lock_unlock():
    """AC: Users must be able to lock and unlock their registered cards."""
    # Lock card crd_001
    res_lock = client.patch("/api/v1/cards/crd_001/status", json={"status": "LOCKED"})
    assert res_lock.status_code == 200
    assert res_lock.json()["status"] == "LOCKED"

    # Unlock card crd_001
    res_unlock = client.patch("/api/v1/cards/crd_001/status", json={"status": "ACTIVE"})
    assert res_unlock.status_code == 200
    assert res_unlock.json()["status"] == "ACTIVE"


def test_update_card_limits():
    """Verify updating spending limits."""
    res = client.patch("/api/v1/cards/crd_001/limits", json={"monthly_limit": 30000.0, "pos_limit": 12000.0})
    assert res.status_code == 200
    data = res.json()
    assert data["monthly_limit"] == 30000.0
    assert data["pos_limit"] == 12000.0
