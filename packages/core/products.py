"""CRUD-операции с товарами и складскими остатками."""
import sqlite3
from typing import List


def get_all(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute(
        "SELECT p.ProductID, p.ProductName, p.Price, p.StockQuantity, "
        "p.WarrantyMonths, c.CategoryName, s.SupplierName "
        "FROM Products p "
        "LEFT JOIN Categories c ON p.CategoryID = c.CategoryID "
        "LEFT JOIN Suppliers  s ON p.SupplierID = s.SupplierID"
    ).fetchall()
    return [dict(r) for r in rows]


def get_available(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute(
        "SELECT ProductID, ProductName, Price, StockQuantity "
        "FROM Products WHERE StockQuantity > 0"
    ).fetchall()
    return [dict(r) for r in rows]


def get_low_stock(conn: sqlite3.Connection, threshold: int = 10) -> List[dict]:
    rows = conn.execute(
        "SELECT ProductName, StockQuantity, Price FROM Products "
        "WHERE StockQuantity < ? ORDER BY StockQuantity",
        (threshold,),
    ).fetchall()
    return [dict(r) for r in rows]


def restock(conn: sqlite3.Connection, product_id: int, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError(f"Количество должно быть > 0, получено: {quantity}")
    conn.execute(
        "UPDATE Products SET StockQuantity = StockQuantity + ? WHERE ProductID = ?",
        (quantity, product_id),
    )
    conn.commit()
