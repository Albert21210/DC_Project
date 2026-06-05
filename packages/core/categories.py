import sqlite3
from typing import List


def get_all(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute(
        "SELECT c.CategoryID, c.CategoryName, c.Description, "
        "COUNT(p.ProductID) AS ProductCount "
        "FROM Categories c "
        "LEFT JOIN Products p ON c.CategoryID = p.CategoryID "
        "GROUP BY c.CategoryID ORDER BY c.CategoryName"
    ).fetchall()
    return [dict(r) for r in rows]
