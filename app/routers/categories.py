from fastapi import APIRouter, Depends
import sqlite3
from app.dependencies import get_db
from packages.core import categories as svc

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/")
def list_categories(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_all(db)