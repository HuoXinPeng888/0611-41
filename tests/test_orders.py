"""Tests that read from the shared database; order-dependent failures."""

from src.db import add_user, get_orders, get_users


class TestOrders:
    """3 tests reading the same session-scoped :memory: DB.

    These tests will pass or fail depending on whether test_users.py
    has already been executed in the same session.
    """

    def test_orders_initially_empty(self, db_session):
        # BUG: Assumes the DB is clean, but test_users.py::test_add_order_for_user
        # may have already inserted an order. The assertion below will FAIL
        # if test_users.py executed first.
        orders = get_orders()
        assert len(orders) == 0

    def test_list_users(self, db_session):
        # BUG: If test_users.py ran first, there will be 3 users (Alice, Bob,
        # Charlie) and this assertion passes. If test_orders.py runs first,
        # the DB has 0 users and it FAILS.
        users = get_users()
        assert len(users) == 3

    def test_new_user_after_orders(self, db_session):
        add_user("Dave")
        users = get_users()
        # BUG: Expected count depends on whether the 3 users from test_users.py
        # already exist. Could be 1 (orders.py runs first), 4 (users.py ran
        # first), or anything else depending on previous mutations.
        assert len(users) == 4
