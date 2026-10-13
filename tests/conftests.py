import pytest
from storage import get_connection


@pytest.fixture(autouse=True)
def use_test_database(monkeypatch):
    monkeypatch.setenv("DB_NAME", "business_expense_tracker_test")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database()")
            db_name = cur.fetchone()[0]

    assert db_name == "business_expense_tracker_test", (
        f"Tests are using '{db_name}' instead of the test database!"
    )

