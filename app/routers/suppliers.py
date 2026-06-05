from fastapi import APIRouter, Depends
import sqlite3
from app.dependencies import get_db
from packages.core import suppliers as svc

router = APIRouter(prefix="/api/suppliers", tags=["suppliers"])


@router.get("/")
def list_suppliers(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_all(db)