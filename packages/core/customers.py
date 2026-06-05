import sqlite3
from typing import List


def get_all(conn: sqlite3.Connection) -> List[dict]:
    rows = conn.execute("SELECT * FROM Customers ORDER BY CustomerID ASC").fetchall()
    return [dict(r) for r in rows]


def create(conn: sqlite3.Connection, last_name: str, first_name: str,
           phone: str, email: str) -> int:
    cur = conn.cursor()
    new_id = (cur.execute("SELECT COALESCE(MAX(CustomerID),0) FROM Customers").fetchone()[0]) + 1
    cur.execute("INSERT INTO Customers VALUES(?,?,?,?,?)",
                (new_id, last_name, first_name, phone, email))
    conn.commit()
    return new_id
