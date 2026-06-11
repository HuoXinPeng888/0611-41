"""Simple in-memory SQLite database module."""

import sqlite3

_connection: sqlite3.Connection | None = None


def init_db() -> None:
    """Create in-memory database with users and orders tables."""
    global _connection
    _connection = sqlite3.connect(":memory:")
    _connection.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
    )
    _connection.execute(
        "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)"
    )
    _connection.commit()


def _get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        init_db()
    return _connection  # type: ignore[return-value]


def add_user(name: str) -> None:
    conn = _get_connection()
    conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()


def get_users() -> list[tuple]:
    conn = _get_connection()
    return conn.execute("SELECT * FROM users").fetchall()


def add_order(user_id: int, amount: float) -> None:
    conn = _get_connection()
    conn.execute("INSERT INTO orders (user_id, amount) VALUES (?, ?)", (user_id, amount))
    conn.commit()


def get_orders() -> list[tuple]:
    conn = _get_connection()
    return conn.execute("SELECT * FROM orders").fetchall()


def reset_db() -> None:
    """Delete all data from tables, keeping the schema intact."""
    conn = _get_connection()
    conn.execute("DELETE FROM orders")
    conn.execute("DELETE FROM users")
    conn.commit()
