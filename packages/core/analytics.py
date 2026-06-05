import sqlite3
from typing import List, Tuple


def top_products(conn: sqlite3.Connection, limit: int = 3) -> List[dict]:
    rows = conn.execute("""
        SELECT p.ProductName, SUM(od.Quantity) AS TotalQty, p.Price
        FROM Order_Details od
        JOIN Products p ON od.ProductID = p.ProductID
        JOIN Orders   o ON od.OrderID   = o.OrderID
        WHERE o.OrderStatus IN ('Оплачен','Выдан')
        GROUP BY p.ProductID ORDER BY TotalQty DESC LIMIT ?
    """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def monthly_revenue(conn: sqlite3.Connection, days: int = 30) -> dict:
    revenue = conn.execute("""
        SELECT COALESCE(SUM(od.Quantity*od.UnitPrice),0)
        FROM Order_Details od JOIN Orders o ON od.OrderID=o.OrderID
        WHERE o.OrderStatus IN ('Оплачен','Выдан')
          AND o.OrderDate >= date('now',? || ' days')
    """, (f"-{days}",)).fetchone()[0]
    count = conn.execute("""
        SELECT COUNT(*) FROM Orders
        WHERE OrderStatus IN ('Оплачен','Выдан')
          AND OrderDate >= date('now',? || ' days')
    """, (f"-{days}",)).fetchone()[0]
    return {"revenue": float(revenue), "count": int(count),
            "avg": round(float(revenue) / count, 2) if count else 0.0}


def order_sums(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute("""
        SELECT o.OrderID, c.LastName||' '||c.FirstName AS Customer,
               o.OrderDate, o.OrderStatus,
               SUM(od.Quantity*od.UnitPrice) AS Total
        FROM Orders o
        JOIN Customers     c  ON o.CustomerID=c.CustomerID
        JOIN Order_Details od ON o.OrderID=od.OrderID
        GROUP BY o.OrderID
    """).fetchall()
    return [dict(r) for r in rows]