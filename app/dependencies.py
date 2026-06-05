import os
from functools import lru_cache
import sqlite3
from packages.core.database import get_connection, init_schema, seed_demo_data

DB_PATH = os.getenv("SHOP_DB_PATH", "shop.db")

@lru_cache(maxsize=1)
def _get_conn() -> sqlite3.Connection:
    conn = get_connection(DB_PATH)
    init_schema(conn)
    seed_demo_data(conn)
    return conn

def get_db() -> sqlite3.Connection:
    return _get_conn()
