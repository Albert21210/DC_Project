"""Тесты отмены заказа."""
import pytest
from packages.core import orders


def test_cancel_changes_status(conn):
    orders.cancel_order(conn, 102)
    status = conn.execute(
        "SELECT OrderStatus FROM Orders WHERE OrderID=102"
    ).fetchone()[0]
    assert status == "Отменён"


def test_cancel_paid_raises(conn):
    with pytest.raises(ValueError, match="Нельзя отменить"):
        orders.cancel_order(conn, 103)  # 103 = Оплачен


def test_cancel_delivered_raises(conn):
    with pytest.raises(ValueError, match="Нельзя отменить"):
        orders.cancel_order(conn, 101)  # 101 = Выдан


def test_cancel_nonexistent_raises(conn):
    with pytest.raises(ValueError):
        orders.cancel_order(conn, 9999)


def test_cancel_api_ok(client):
    r = client.post("/api/orders/102/cancel")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_cancel_api_paid_400(client):
    r = client.post("/api/orders/103/cancel")
    assert r.status_code == 400


def test_cancel_removes_from_unpaid(client):
    client.post("/api/orders/102/cancel")
    ids = [o["OrderID"] for o in client.get("/api/orders/unpaid").json()]
    assert 102 not in ids
