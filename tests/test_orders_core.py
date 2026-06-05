"""Тесты packages.core.orders."""
import pytest
from packages.core import orders

CART = {1: {"qty": 1, "price": 18500.0, "name": "i5"}}
CART2 = {1: {"qty": 1, "price": 18500.0, "name": "i5"},
         4: {"qty": 2, "price": 13000.0, "name": "RAM"}}


def test_create_returns_int(conn):
    oid = orders.create(conn, 1, 1, CART)
    assert isinstance(oid, int) and oid > 0


def test_create_sequential_ids(conn):
    id1 = orders.create(conn, 1, 1, CART)
    id2 = orders.create(conn, 2, 2, {4: {"qty": 1, "price": 13000.0, "name": "RAM"}})
    assert id2 == id1 + 1


def test_create_decreases_stock(conn):
    before = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    orders.create(conn, 1, 1, CART)
    after = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    assert after == before - 1


def test_create_multi_item_stock(conn):
    b1 = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    b4 = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=4").fetchone()[0]
    orders.create(conn, 1, 1, CART2)
    a1 = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    a4 = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=4").fetchone()[0]
    assert a1 == b1 - 1 and a4 == b4 - 2


def test_create_raises_empty_cart(conn):
    with pytest.raises(ValueError):
        orders.create(conn, 1, 1, {})


def test_get_all_includes_demo_orders(conn):
    ids = {r["OrderID"] for r in orders.get_all(conn)}
    assert {101, 102, 103}.issubset(ids)


def test_get_unpaid_has_order_102(conn):
    ids = [r["OrderID"] for r in orders.get_unpaid(conn)]
    assert 102 in ids


def test_confirm_payment_changes_status(conn):
    orders.confirm_payment(conn, 102)
    status = conn.execute("SELECT OrderStatus FROM Orders WHERE OrderID=102").fetchone()[0]
    assert status == "Оплачен"


def test_confirm_payment_removes_from_unpaid(conn):
    orders.confirm_payment(conn, 102)
    ids = [r["OrderID"] for r in orders.get_unpaid(conn)]
    assert 102 not in ids
