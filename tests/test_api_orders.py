"""HTTP-тесты /api/orders."""

CART = {"1": {"qty": 1, "price": 18500.0, "name": "i5"}}


def test_list_orders_200(client):
    r = client.get("/api/orders/")
    assert r.status_code == 200
    assert len(r.json()) >= 3


def test_list_orders_has_fields(client):
    item = client.get("/api/orders/").json()[0]
    for f in ("OrderID", "Customer", "OrderStatus", "Total"):
        assert f in item


def test_unpaid_contains_102(client):
    ids = [r["OrderID"] for r in client.get("/api/orders/unpaid").json()]
    assert 102 in ids


def test_create_order_ok(client):
    r = client.post("/api/orders/", json={"customer_id": 1, "employee_id": 1, "cart": CART})
    assert r.status_code == 200
    assert "order_id" in r.json()


def test_create_order_empty_cart_400(client):
    r = client.post("/api/orders/", json={"customer_id": 1, "employee_id": 1, "cart": {}})
    assert r.status_code == 400


def test_pay_order_ok(client):
    r = client.post("/api/orders/102/pay")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_pay_removes_from_unpaid(client):
    client.post("/api/orders/102/pay")
    ids = [r["OrderID"] for r in client.get("/api/orders/unpaid").json()]
    assert 102 not in ids


def test_get_order_detail_200(client):
    r = client.get("/api/orders/101")
    assert r.status_code == 200
    data = r.json()
    assert "order" in data and "details" in data


def test_get_order_detail_has_lines(client):
    r = client.get("/api/orders/101")
    assert len(r.json()["details"]) >= 1


def test_get_order_detail_404(client):
    r = client.get("/api/orders/9999")
    assert r.status_code == 404


def test_filter_by_status_oformlen(client):
    r = client.get("/api/orders/?status=Оформлен")
    assert r.status_code == 200
    assert all(o["OrderStatus"] == "Оформлен" for o in r.json())


def test_filter_by_status_vydan(client):
    r = client.get("/api/orders/?status=Выдан")
    assert all(o["OrderStatus"] == "Выдан" for o in r.json())


def test_filter_empty_returns_all(client):
    r = client.get("/api/orders/?status=")
    assert len(r.json()) >= 3


def test_pagination_limit(client):
    r = client.get("/api/orders/?limit=2")
    assert r.status_code == 200
    assert len(r.json()) <= 2


def test_pagination_skip(client):
    all_orders = client.get("/api/orders/").json()
    skipped = client.get("/api/orders/?skip=1").json()
    if len(all_orders) > 1:
        assert all_orders[1]["OrderID"] == skipped[0]["OrderID"]
