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


def create(conn: sqlite3.Connection, customer_id: int,
           employee_id: int, cart: Dict[int, dict]) -> int:
    if not cart:
        raise ValueError("Корзина пустая")
    today = datetime.date.today().isoformat()
    cur = conn.cursor()
    try:
        new_id = (cur.execute("SELECT COALESCE(MAX(OrderID),100) FROM Orders").fetchone()[0]) + 1
        cur.execute("INSERT INTO Orders VALUES(?,?,?,?,'Оформлен')",
                    (new_id, customer_id, employee_id, today))
        det_id = cur.execute("SELECT COALESCE(MAX(OrderDetailID),0) FROM Order_Details").fetchone()[0]
        for pid, item in cart.items():
            det_id += 1
            cur.execute("INSERT INTO Order_Details VALUES(?,?,?,?,?)",
                        (det_id, new_id, pid, item["qty"], item["price"]))
            cur.execute("UPDATE Products SET StockQuantity=StockQuantity-? WHERE ProductID=?",
                        (item["qty"], pid))
        conn.commit()
        return new_id
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Ошибка создания заказа: {e}") from e