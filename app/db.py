import os
import sqlite3
from typing import Any, List, Optional


def get_db_file() -> str:
    return os.getenv("DATABASE_FILE", "banking.db")


def get_connection() -> sqlite3.Connection:
    db_path = get_db_file()
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(schema_path: Optional[str] = None, seed_path: Optional[str] = None) -> None:
    if not schema_path:
        schema_path = os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql")
    if not seed_path:
        seed_path = os.path.join(os.path.dirname(__file__), "..", "db", "seed.sql")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())

        if os.path.exists(seed_path):
            with open(seed_path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
        conn.commit()
    finally:
        conn.close()


def query_all(query: str, params: tuple = ()) -> List[dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def query_one(query: str, params: tuple = ()) -> Optional[dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def execute_mutation(query: str, params: tuple = ()) -> Any:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
