from fastapi import APIRouter, Depends
import sqlite3
from app.dependencies import get_db
from packages.core import employees as svc

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("/")
def list_employees(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_all(db)
