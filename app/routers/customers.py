from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlite3
from app.dependencies import get_db
from packages.core import customers as svc

router = APIRouter(prefix="/api/customers", tags=["customers"])


class CustomerIn(BaseModel):
    last_name: str
    first_name: str
    phone: str = ""
    email: str = ""


@router.get("/")
def list_customers(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_all(db)


@router.post("/")
def create_customer(body: CustomerIn, db: sqlite3.Connection = Depends(get_db)):
    cid = svc.create(db, body.last_name, body.first_name, body.phone, body.email)
    return {"ok": True, "customer_id": cid}
