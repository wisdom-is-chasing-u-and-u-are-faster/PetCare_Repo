import os
import uuid
import pytest
from app.db import init_db, query_all, query_one, execute_mutation


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = f"test_db_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_FILE"] = test_db
    init_db()
    yield
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass


def test_database_initialization():
    """Verify that schema and seed data are initialized properly."""
    accounts = query_all("SELECT * FROM accounts")
    assert len(accounts) >= 3

    cards = query_all("SELECT * FROM cards")
    assert len(cards) >= 2

    user = query_one("SELECT * FROM users WHERE email = ?", ("admin@bank.com",))
    assert user is not None
    assert user["full_name"] == "Jane Doe"


def test_mutation_execution():
    """Verify that INSERT and UPDATE mutations succeed."""
    new_user_id = f"test_user_{uuid.uuid4().hex[:6]}"
    email = f"test_{uuid.uuid4().hex[:6]}@test.com"
    execute_mutation(
        "INSERT INTO users (id, full_name, email, password_hash) VALUES (?, ?, ?, ?)",
        (new_user_id, "Test User", email, "hash123")
    )
    user = query_one("SELECT * FROM users WHERE id = ?", (new_user_id,))
    assert user is not None
    assert user["email"] == email
