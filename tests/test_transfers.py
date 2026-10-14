import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_transfers_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_initiate_transfer_success():
    """AC: Users must be able to initiate a domestic fund transfer."""
    payload = {
        "from_account_id": "acc_001",
        "to_account_id": "acc_002",
        "amount": 500.0,
        "transfer_type": "Internal Transfer",
        "memo": "Test internal transfer",
        "idempotency_key": f"unique_idem_test_{uuid.uuid4().hex[:6]}"
    }
    response = client.post("/api/v1/transfers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert "reference_number" in data
    assert data["amount"] == 500.0


def test_transfer_idempotency():
    """Verify that submitting with the same idempotency key returns cached transfer."""
    idem_key = f"idem_dup_{uuid.uuid4().hex[:6]}"
    payload = {
        "from_account_id": "acc_001",
        "to_account_id": "acc_002",
        "amount": 250.0,
        "transfer_type": "ACH",
        "memo": "Idempotency test",
        "idempotency_key": idem_key
    }
    res1 = client.post("/api/v1/transfers", json=payload)
    assert res1.status_code == 201
    ref1 = res1.json()["reference_number"]

    res2 = client.post("/api/v1/transfers", json=payload)
    assert res2.status_code == 201
    ref2 = res2.json()["reference_number"]
    assert ref1 == ref2


def test_transfer_insufficient_funds():
    """Verify error when account balance is less than transfer amount."""
    payload = {
        "from_account_id": "acc_001",
        "to_account_id": "acc_002",
        "amount": 999999999.0,
        "transfer_type": "Domestic Wire"
    }
    response = client.post("/api/v1/transfers", json=payload)
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]


def test_list_transfers():
    """Verify listing recent transfers."""
    response = client.get("/api/v1/transfers")
    assert response.status_code == 200
    data = response.json()
    assert "transfers" in data
