"""Tests for user operations — each test is fully self-contained."""

from src.db import add_order, add_user, get_users, get_orders


class TestUsers:
    """Each test sets up its own data so execution order doesn't matter."""

    def test_add_first_user(self, db_session):
        add_user("Alice")
        users = get_users()
        assert len(users) == 1
        assert users[0][1] == "Alice"

    def test_add_second_user(self, db_session):
        add_user("Alice")
        add_user("Bob")
        users = get_users()
        assert len(users) == 2
        assert users[-1][1] == "Bob"

    def test_user_count_increases(self, db_session):
        add_user("Alice")
        add_user("Bob")
        add_user("Charlie")
        users = get_users()
        assert len(users) == 3
        assert users[-1][1] == "Charlie"

    def test_add_order_for_user(self, db_session):
        add_user("Alice")
        add_order(1, 100.0)
        orders = get_orders()
        assert len(orders) == 1
