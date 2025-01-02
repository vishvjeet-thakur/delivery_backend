from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.delivery import Delivery
from app.db import get_session
from datetime import datetime

router = APIRouter()

#Delivery - Basically when assigning delivery man to the orders, when a order is delivered, when it is assigned to a delivery boy etc.

@router.post("/")  # to create a new delivery
def create_delivery(delivery: Delivery, session: Session = Depends(get_session)):
    delivery.order_placed_at=datetime.now()
    session.add(delivery)
    session.commit()
    session.refresh(delivery)
    return delivery

@router.get("/{delivery_id}/") # to get a delivery by delivery_id
def view_delivery_details(delivery_id: int, session: Session = Depends(get_session)):
    delivery = session.get(Delivery, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@router.get('/') # to get all deliveries
def view_all_delivery(session:Session=Depends(get_session)):
    deliveries = session.exec(select(Delivery)).all()
    return deliveries