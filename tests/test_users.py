"""Tests that mutate shared database state."""

from src.db import add_order, add_user, get_users


class TestUsers:
    """4 tests that insert data into the session-scoped :memory: DB.

    Because the DB is shared, each test leaves permanent traces that subsequent
    tests (in this file *or* in test_orders.py) will observe.
    """

    def test_add_first_user(self, db_session):
        add_user("Alice")
        users = get_users()
        assert len(users) == 1
        assert users[0][1] == "Alice"

    def test_add_second_user(self, db_session):
        add_user("Bob")
        users = get_users()
        # BUG: This assertion assumes test_add_first_user already ran.
        # If this test executes first (or in isolation via --no-header -k),
        # len(users) will be 1, not 2.
        assert len(users) == 2
        assert users[-1][1] == "Bob"

    def test_user_count_increases(self, db_session):
        add_user("Charlie")
        users = get_users()
        # BUG: Same problem — passes only when both previous tests ran first.
        # Expected count 3 depends on Alice and Bob already inserted.
        assert len(users) == 3
        assert users[-1][1] == "Charlie"

    def test_add_order_for_user(self, db_session):
        add_order(1, 100.0)
        from src.db import get_orders

        orders = get_orders()
        assert len(orders) == 1  # passes in any order within this file
