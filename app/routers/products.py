from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import sqlite3
from app.dependencies import get_db
from packages.core import products as svc

router = APIRouter(prefix="/api/products", tags=["products"])


class RestockIn(BaseModel):
    product_id: int
    quantity: int


@router.get("/")
def list_products(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_all(db)


@router.get("/by-category/{category_id}")
def by_category(category_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Товары определённой категории."""
    rows = db.execute(
        "SELECT p.ProductID, p.ProductName, p.Price, p.StockQuantity, "
        "p.WarrantyMonths, c.CategoryName, s.SupplierName "
        "FROM Products p "
        "LEFT JOIN Categories c ON p.CategoryID=c.CategoryID "
        "LEFT JOIN Suppliers  s ON p.SupplierID=s.SupplierID "
        "WHERE p.CategoryID=?",
        (category_id,),
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/search")
def search_products(q: str = "", db: sqlite3.Connection = Depends(get_db)):
    """Поиск товаров по названию (регистронезависимый)."""
    rows = db.execute(
        "SELECT ProductID, ProductName, Price, StockQuantity FROM Products "
        "WHERE ProductName LIKE ?", (f"%{q}%",)
    ).fetchall()
    return [dict(r) for r in rows]


@router.get("/available")
def available_products(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_available(db)


@router.get("/low-stock")
def low_stock(threshold: int = 10, db: sqlite3.Connection = Depends(get_db)):
    return svc.get_low_stock(db, threshold)


@router.post("/restock")
def restock(body: RestockIn, db: sqlite3.Connection = Depends(get_db)):
    try:
        svc.restock(db, body.product_id, body.quantity)
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(400, str(e))
