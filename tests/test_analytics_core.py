"""Тесты packages.core.analytics."""
from packages.core import analytics


def test_top_products_limit(conn):
    assert len(analytics.top_products(conn, limit=3)) <= 3


def test_top_products_sorted_desc(conn):
    qtys = [r["TotalQty"] for r in analytics.top_products(conn, limit=5)]
    assert qtys == sorted(qtys, reverse=True)


def test_monthly_revenue_keys(conn):
    res = analytics.monthly_revenue(conn)
    assert "revenue" in res and "count" in res and "avg" in res


def test_monthly_revenue_non_negative(conn):
    res = analytics.monthly_revenue(conn)
    assert res["revenue"] >= 0 and res["count"] >= 0


def test_monthly_avg_correct(conn):
    res = analytics.monthly_revenue(conn)
    if res["count"]:
        assert abs(res["avg"] - res["revenue"] / res["count"]) < 0.01


def test_order_sums_all_orders(conn):
    ids = {r["OrderID"] for r in analytics.order_sums(conn)}
    assert {101, 102, 103}.issubset(ids)


def test_employee_efficiency_positive_revenue(conn):
    for r in analytics.employee_efficiency(conn):
        assert r["Revenue"] > 0
