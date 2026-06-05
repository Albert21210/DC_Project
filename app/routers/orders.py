from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
import sqlite3
from app.dependencies import get_db
from packages.core import orders as svc

router = APIRouter(prefix="/api/orders", tags=["orders"])


class CartItem(BaseModel):
    qty: int
    price: float
    name: str = ""


class CreateOrderIn(BaseModel):
    customer_id: int
    employee_id: int
    cart: Dict[int, CartItem]


@router.get("/")
def list_orders(status: str = "", skip: int = 0, limit: int = 50,
                  db: sqlite3.Connection = Depends(get_db)):
    """Список заказов с фильтром по статусу и пагинацией."""
    data = svc.get_all(db)
    if status:
        data = [o for o in data if o["OrderStatus"] == status]
    return data[skip: skip + limit]


@router.get("/unpaid")
def unpaid_orders(db: sqlite3.Connection = Depends(get_db)):
    return svc.get_unpaid(db)


@router.post("/")
def create_order(body: CreateOrderIn, db: sqlite3.Connection = Depends(get_db)):
    cart = {pid: item.model_dump() for pid, item in body.cart.items()}
    try:
        order_id = svc.create(db, body.customer_id, body.employee_id, cart)
        return {"ok": True, "order_id": order_id}
    except (ValueError, RuntimeError) as e:
        raise HTTPException(400, str(e))


@router.post("/{order_id}/pay")
def pay_order(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        svc.confirm_payment(db, order_id)
        return {"ok": True}
    except RuntimeError as e:
        raise HTTPException(400, str(e))


@router.get("/{order_id}")
def get_order(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Возвращает детали одного заказа с позициями."""
    order = db.execute(
        "SELECT o.*, c.LastName||' '||c.FirstName AS Customer "
        "FROM Orders o LEFT JOIN Customers c ON o.CustomerID=c.CustomerID "
        "WHERE o.OrderID=?", (order_id,)
    ).fetchone()
    if not order:
        raise HTTPException(404, "Заказ не найден")
    details = db.execute(
        "SELECT od.*, p.ProductName FROM Order_Details od "
        "JOIN Products p ON od.ProductID=p.ProductID WHERE od.OrderID=?",
        (order_id,)
    ).fetchall()
    return {"order": dict(order), "details": [dict(d) for d in details]}


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Отменяет заказ (только если статус «Оформлен»)."""
    try:
        svc.cancel_order(db, order_id)
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except RuntimeError as e:
        raise HTTPException(500, str(e))
