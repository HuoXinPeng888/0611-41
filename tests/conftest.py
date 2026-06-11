"""Per-test isolated fixtures."""

import pytest

from src.db import init_db


@pytest.fixture(autouse=True)
def db_session(monkeypatch):
    """Give every test a fresh in-memory database and clean environment."""
    # --- env isolation ---------------------------------------------------
    # Remove APP_MODE so tests start from a clean slate; monkeypatch
    # automatically restores the original value after each test.
    monkeypatch.delenv("APP_MODE", raising=False)

    # --- DB isolation ----------------------------------------------------
    # Close any leftover connection from a previous test, then re-init.
    import src.db as db_module

    if db_module._connection is not None:
        db_module._connection.close()
        db_module._connection = None

    init_db()

    yield

    # Teardown: drop tables and close so nothing leaks to the next test.
    conn = db_module._connection
    if conn is not None:
        conn.execute("DROP TABLE IF EXISTS orders")
        conn.execute("DROP TABLE IF EXISTS users")
        conn.close()
        db_module._connection = None
