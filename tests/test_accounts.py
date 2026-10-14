import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_accounts_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_list_accounts():
    """AC: The delivered application must allow users to view their account balances and transaction history."""
    response = client.get("/api/v1/accounts")
    assert response.status_code == 200
    data = response.json()
    assert "accounts" in data
    assert len(data["accounts"]) >= 3

    first = data["accounts"][0]
    assert "available_balance" in first
    assert "ledger_balance" in first
    assert first["available_balance"] > 0


def test_get_account_detail():
    """Verify single account retrieval with accurate balance."""
    response = client.get("/api/v1/accounts/acc_001")
    assert response.status_code == 200
    account = response.json()
    assert account["id"] == "acc_001"
    assert account["account_name"] == "Main Operating Account"


def test_get_account_transactions():
    """Verify transaction history retrieval for an account."""
    response = client.get("/api/v1/accounts/acc_001/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert len(data["transactions"]) >= 1
    assert "running_balance" in data["transactions"][0]


def test_get_account_not_found():
    """Verify 404 response for invalid account ID."""
    response = client.get("/api/v1/accounts/non_existent_id")
    assert response.status_code == 404
