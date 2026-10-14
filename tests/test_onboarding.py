import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_onboarding_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_customer_onboarding_ekyc():
    """AC: The application must provide a flow for new users to onboard."""
    payload = {
        "company_name": "Apex Global Fintech LLC",
        "full_name": "Robert Vance",
        "work_email": f"robert_{uuid.uuid4().hex[:6]}@apexfintech.com",
        "id_document": "passport_scan.pdf",
        "address_document": "utility_bill.pdf"
    }
    response = client.post("/api/v1/onboarding", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "APPROVED"
    assert "application_id" in data


def test_login_success():
    """Verify sign in with valid credentials."""
    response = client.post("/api/v1/auth/login", json={"email": "admin@bank.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["full_name"] == "Jane Doe"


def test_login_invalid():
    """Verify 401 on bad credentials."""
    response = client.post("/api/v1/auth/login", json={"email": "bad@bank.com", "password": "wrongpassword"})
    assert response.status_code == 401
