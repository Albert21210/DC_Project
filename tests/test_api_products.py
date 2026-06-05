"""HTTP-тесты /api/products."""


def test_list_products_200(client):
    r = client.get("/api/products/")
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_list_products_has_fields(client):
    item = client.get("/api/products/").json()[0]
    for f in ("ProductID", "ProductName", "Price", "StockQuantity"):
        assert f in item


def test_available_products_positive_stock(client):
    items = client.get("/api/products/available").json()
    assert all(i["StockQuantity"] > 0 for i in items)


def test_low_stock_default(client):
    items = client.get("/api/products/low-stock").json()
    assert all(i["StockQuantity"] < 10 for i in items)


def test_low_stock_custom_threshold(client):
    items = client.get("/api/products/low-stock?threshold=5").json()
    assert all(i["StockQuantity"] < 5 for i in items)


def test_restock_ok(client):
    r = client.post("/api/products/restock", json={"product_id": 1, "quantity": 5})
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_restock_updates_stock(client):
    before = next(p["StockQuantity"] for p in client.get("/api/products/").json() if p["ProductID"] == 1)
    client.post("/api/products/restock", json={"product_id": 1, "quantity": 3})
    after = next(p["StockQuantity"] for p in client.get("/api/products/").json() if p["ProductID"] == 1)
    assert after == before + 3


def test_restock_zero_qty_400(client):
    r = client.post("/api/products/restock", json={"product_id": 1, "quantity": 0})
    assert r.status_code == 400


def test_search_by_name(client):
    r = client.get("/api/products/search?q=Intel")
    assert r.status_code == 200
    assert all("Intel" in i["ProductName"] for i in r.json())


def test_search_empty_returns_all(client):
    r = client.get("/api/products/search?q=")
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_search_no_match_returns_empty(client):
    r = client.get("/api/products/search?q=Ничего_такого")
    assert r.status_code == 200
    assert r.json() == []


def test_by_category_returns_correct(client):
    r = client.get("/api/products/by-category/1")  # Процессоры
    assert r.status_code == 200
    assert len(r.json()) == 2  # Intel i5 + AMD Ryzen


def test_by_category_empty_for_unknown(client):
    r = client.get("/api/products/by-category/999")
    assert r.status_code == 200
    assert r.json() == []
