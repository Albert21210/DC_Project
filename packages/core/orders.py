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
    

def confirm_payment(conn: sqlite3.Connection, order_id: int) -> None:
    try:
        conn.execute("UPDATE Orders SET OrderStatus='Оплачен' WHERE OrderID=?", (order_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(str(e)) from e


def cancel_order(conn: sqlite3.Connection, order_id: int) -> None:
    """Отменяет заказ — ставит статус «Отменён».

    Raises:
        ValueError:   если заказ уже оплачен или выдан.
        RuntimeError: при ошибке БД.
    """
    row = conn.execute(
        "SELECT OrderStatus FROM Orders WHERE OrderID=?", (order_id,)
    ).fetchone()
    if not row:
        raise ValueError(f"Заказ №{order_id} не найден")
    if row[0] in ("Оплачен", "Выдан"):
        raise ValueError(f"Нельзя отменить заказ со статусом «{row[0]}»")
    try:
        conn.execute(
            "UPDATE Orders SET OrderStatus='Отменён' WHERE OrderID=?", (order_id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(str(e)) from e