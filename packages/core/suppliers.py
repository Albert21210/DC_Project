import sqlite3
from typing import List


def get_all(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute("SELECT * FROM Suppliers ORDER BY SupplierID ASC").fetchall()
    return [dict(r) for r in rows]
