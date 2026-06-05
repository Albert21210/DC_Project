"""Тесты packages.core.products."""
import pytest
from packages.core import products


def test_get_all_returns_five(conn):
    assert len(products.get_all(conn)) == 5


def test_get_all_has_category_name(conn):
    row = products.get_all(conn)[0]
    assert "CategoryName" in row


def test_available_excludes_zero(conn):
    conn.execute("UPDATE Products SET StockQuantity=0 WHERE ProductID=1")
    ids = [r["ProductID"] for r in products.get_available(conn)]
    assert 1 not in ids


def test_available_all_positive(conn):
    assert all(r["StockQuantity"] > 0 for r in products.get_available(conn))


def test_low_stock_default_threshold(conn):
    result = products.get_low_stock(conn)
    assert all(r["StockQuantity"] < 10 for r in result)


def test_low_stock_custom_threshold(conn):
    result = products.get_low_stock(conn, threshold=5)
    assert all(r["StockQuantity"] < 5 for r in result)


def test_low_stock_sorted_asc(conn):
    qtys = [r["StockQuantity"] for r in products.get_low_stock(conn)]
    assert qtys == sorted(qtys)


def test_restock_increases_qty(conn):
    before = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    products.restock(conn, 1, 10)
    after = conn.execute("SELECT StockQuantity FROM Products WHERE ProductID=1").fetchone()[0]
    assert after == before + 10


def test_restock_raises_on_zero(conn):
    with pytest.raises(ValueError):
        products.restock(conn, 1, 0)


def test_restock_raises_on_negative(conn):
    with pytest.raises(ValueError):
        products.restock(conn, 1, -3)
