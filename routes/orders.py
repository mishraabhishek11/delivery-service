from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Order, OrderCreate, OrderStatus, OrderUpdate, StatusLog
from sqlmodel import Session, select
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
def create_order(order_create: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(
        customer_name=order_create.customer_name,
        delivery_address=order_create.delivery_address,
        items=order_create.items,
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order


@router.get("/", response_model=list[Order])
def list_orders(status: OrderStatus | None = Query(default=None, description="Filter orders by status"),
                created_at: str | None = Query(
        default=None, description="Filter orders by creation date (YYYY-MM-DD)"),
        skip: int = Query(
        default=0, description="Number of records to skip", ge=1),
        limit: int = Query(
        default=10, description="Maximum number of records to return", ge=1, le=100),
        session: Session = Depends(get_session)):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)

    if created_at:
        start = datetime.combine(created_at, datetime.min.time())
        end = datetime.combine(created_at, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()
