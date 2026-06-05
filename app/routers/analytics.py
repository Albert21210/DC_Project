from fastapi import APIRouter, Depends
import sqlite3
from app.dependencies import get_db
from packages.core import analytics as svc

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/top-products")
def top_products(limit: int = 3, db: sqlite3.Connection = Depends(get_db)):
    return svc.top_products(db, limit)


@router.get("/monthly-revenue")
def monthly_revenue(days: int = 30, db: sqlite3.Connection = Depends(get_db)):
    return svc.monthly_revenue(db, days)


@router.get("/order-sums")
def order_sums(db: sqlite3.Connection = Depends(get_db)):
    return svc.order_sums(db)


@router.get("/employee-efficiency")
def employee_efficiency(db: sqlite3.Connection = Depends(get_db)):
    return svc.employee_efficiency(db)


@router.get("/summary")
def summary(db: sqlite3.Connection = Depends(get_db)):
    """Сводная статистика для дашборда."""
    products_count = db.execute("SELECT COUNT(*) FROM Products").fetchone()[0]
    customers_count = db.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
    orders_today = db.execute(
        "SELECT COUNT(*) FROM Orders WHERE OrderDate = date('now')"
    ).fetchone()[0]
    low_stock_count = db.execute(
        "SELECT COUNT(*) FROM Products WHERE StockQuantity < 10"
    ).fetchone()[0]
    return {
        "products": products_count,
        "customers": customers_count,
        "orders_today": orders_today,
        "low_stock": low_stock_count,
    }


@router.get("/revenue-by-category")
def revenue_by_category(db: sqlite3.Connection = Depends(get_db)):
    return svc.revenue_by_category(db)
