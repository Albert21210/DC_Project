"""HTTP-тесты /api/analytics."""


def test_top_products_200(client):
    r = client.get("/api/analytics/top-products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_top_products_limit(client):
    r = client.get("/api/analytics/top-products?limit=2")
    assert len(r.json()) <= 2


def test_monthly_revenue_200(client):
    r = client.get("/api/analytics/monthly-revenue")
    assert r.status_code == 200
    data = r.json()
    assert "revenue" in data and "count" in data and "avg" in data


def test_order_sums_200(client):
    r = client.get("/api/analytics/order-sums")
    assert r.status_code == 200
    ids = {i["OrderID"] for i in r.json()}
    assert {101, 102, 103}.issubset(ids)


def test_employee_efficiency_200(client):
    r = client.get("/api/analytics/employee-efficiency")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_summary_200(client):
    r = client.get("/api/analytics/summary")
    assert r.status_code == 200


def test_summary_has_required_keys(client):
    data = client.get("/api/analytics/summary").json()
    for key in ("products", "customers", "orders_today", "low_stock"):
        assert key in data


def test_summary_products_count(client):
    data = client.get("/api/analytics/summary").json()
    assert data["products"] == 5


def test_summary_customers_count(client):
    data = client.get("/api/analytics/summary").json()
    assert data["customers"] == 3


def test_revenue_by_category_200(client):
    r = client.get("/api/analytics/revenue-by-category")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_revenue_by_category_has_fields(client):
    data = client.get("/api/analytics/revenue-by-category").json()
    if data:
        for key in ("CategoryName", "Revenue", "TotalQty"):
            assert key in data[0]


def test_revenue_by_category_sorted_desc(client):
    data = client.get("/api/analytics/revenue-by-category").json()
    revenues = [r["Revenue"] for r in data]
    assert revenues == sorted(revenues, reverse=True)
