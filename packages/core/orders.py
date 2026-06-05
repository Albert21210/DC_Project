import sqlite3
import datetime
from typing import Dict, List

ORDER_STATUSES = ("Оформлен", "Оплачен", "Выдан", "Отменён")


def get_all(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute("""
        SELECT o.OrderID, c.LastName||' '||c.FirstName AS Customer,
               e.LastName||' '||e.FirstName AS Employee,
               o.OrderDate, o.OrderStatus,
               COALESCE(SUM(od.Quantity*od.UnitPrice),0) AS Total
        FROM Orders o
        LEFT JOIN Customers    c  ON o.CustomerID = c.CustomerID
        LEFT JOIN Employees    e  ON o.EmployeeID = e.EmployeeID
        LEFT JOIN Order_Details od ON o.OrderID  = od.OrderID
        GROUP BY o.OrderID ORDER BY o.OrderID ASC
    """).fetchall()
    return [dict(r) for r in rows]


def get_unpaid(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute("""
        SELECT o.OrderID, c.LastName||' '||c.FirstName AS Customer,
               SUM(od.Quantity*od.UnitPrice) AS Total
        FROM Orders o
        JOIN Customers     c  ON o.CustomerID = c.CustomerID
        JOIN Order_Details od ON o.OrderID   = od.OrderID
        WHERE o.OrderStatus = 'Оформлен'
        GROUP BY o.OrderID
    """).fetchall()
    return [dict(r) for r in rows]