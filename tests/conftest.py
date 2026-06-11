"""Per-test fixture that provides a clean database and environment."""

import os

import pytest

from src.db import init_db, reset_db


@pytest.fixture(autouse=True)
def db_session():
    """Give every test a clean database and a controlled APP_MODE."""
    init_db()
    reset_db()

    old_mode = os.environ.get("APP_MODE")
    os.environ["APP_MODE"] = "development"

    yield

    # Restore original environment
    if old_mode is None:
        os.environ.pop("APP_MODE", None)
    else:
        os.environ["APP_MODE"] = old_mode
