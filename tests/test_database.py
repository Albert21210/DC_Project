"""Тесты packages.core.database."""
from packages.core.database import get_connection, init_schema, seed_demo_data


def test_connection_ok():
    conn = get_connection(":memory:")
    assert conn is not None
    conn.close()


def test_foreign_keys_on():
    conn = get_connection(":memory:")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.close()


def test_row_factory_returns_dict_like():
    conn = get_connection(":memory:")
    init_schema(conn)
    seed_demo_data(conn)
    row = conn.execute("SELECT * FROM Categories LIMIT 1").fetchone()
    assert row["CategoryName"] is not None
    conn.close()


def test_schema_creates_all_tables(conn):
    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    for t in ("Categories","Suppliers","Products","Employees","Customers","Orders","Order_Details"):
        assert t in tables


def test_trigger_exists(conn):
    trgs = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger'").fetchall()}
    assert "tg_restore_stock" in trgs


def test_seed_populates_products(conn):
    assert conn.execute("SELECT COUNT(*) FROM Products").fetchone()[0] == 5


def test_seed_idempotent(conn):
    seed_demo_data(conn)
    assert conn.execute("SELECT COUNT(*) FROM Products").fetchone()[0] == 5
