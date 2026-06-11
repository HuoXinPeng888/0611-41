"""Session-scoped fixture with intentional bugs."""

import os

import pytest

from src.config import get_config
from src.db import init_db


@pytest.fixture(scope="session")
def db_session():
    # BUG: shared session DB
    # A single :memory: SQLite connection is created once and shared across
    # ALL tests in ALL test files. Tests that mutate the DB (insert/update)
    # permanently change the global state for subsequent tests.
    init_db()

    # BUG: environ not restored
    # os.environ is modified without using monkeypatch, so the change
    # leaks across the entire test session and is never reverted.
    os.environ["APP_MODE"] = "development"

    yield

    # Missing cleanup:
    #   1. No del os.environ["APP_MODE"] or restore of old value.
    #   2. No teardown / table DROP on the shared in-memory DB.
    #      Once yielded, the connection stays alive and all accumulated data
    #      from every test remains available to any later test.

    # Sanity check: config reads the leaked env var (proving no cleanup)
    cfg = get_config()
    assert cfg["APP_MODE"] == "development", (
        "environ was supposed to be cleaned up but it's still set"
    )
