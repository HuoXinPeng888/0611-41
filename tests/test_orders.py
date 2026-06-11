"""Tests for order operations — each test is fully self-contained."""

from src.db import add_user, get_orders, get_users, add_order


class TestOrders:
    """Each test sets up its own data so execution order doesn't matter."""

    def test_orders_initially_empty(self, db_session):
        orders = get_orders()
        assert len(orders) == 0

    def test_list_users(self, db_session):
        add_user("Alice")
        add_user("Bob")
        add_user("Charlie")
        users = get_users()
        assert len(users) == 3

    def test_new_user_after_orders(self, db_session):
        add_user("Alice")
        add_user("Bob")
        add_user("Charlie")
        add_order(1, 50.0)
        add_user("Dave")
        users = get_users()
        assert len(users) == 4
