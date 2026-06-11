"""Tests for order queries and user listing."""

from src.db import add_order, add_user, get_orders, get_users


class TestOrders:

    def test_orders_initially_empty(self):
        orders = get_orders()
        assert len(orders) == 0

    def test_list_users(self):
        add_user("Alice")
        add_user("Bob")
        add_user("Charlie")
        users = get_users()
        assert len(users) == 3

    def test_new_user_after_orders(self):
        add_user("Alice")
        add_user("Bob")
        add_user("Charlie")
        add_order(1, 50.0)
        add_user("Dave")
        users = get_users()
        assert len(users) == 4
