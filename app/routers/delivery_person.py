from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.delivery_partner import DeliveryBoy
from app.models.order import Order
from app.db import get_session

router = APIRouter()

@router.post("/") # to register a new delivery boy
def register_delivery_boy(deliveryboy: DeliveryBoy, session: Session = Depends(get_session)):
    session.add(deliveryboy)
    session.commit()
    session.refresh(deliveryboy)
    return deliveryboy

@router.patch("/{deliveryboy_id}/{status}/") # to update status of a delivery_boy   like available , in delivery, at the store or inactive right now
def update_status(deliveryboy_id: int, status: str, session: Session = Depends(get_session)):
    deliveryboy = session.get(DeliveryBoy, deliveryboy_id)
    if not deliveryboy:
        raise HTTPException(status_code=404, detail="Delivery Boy not found")
    deliveryboy.status = status
    session.add(deliveryboy)
    session.commit()
    session.refresh(deliveryboy)
    return deliveryboy

@router.get('/{deliveryboy_id}/') # to get a deliveryboy from its id
def get_delivery_boy(deliveryboy_id:int, session:Session = Depends(get_session)):
    deliveryboy = session.get(DeliveryBoy,deliveryboy_id)
    if not deliveryboy:
        raise HTTPException(status_code=404, detail="Delivery Boy not found")
    return deliveryboy
    
@router.get('/') # to get all delivery boys
def get_all_delivery_persons(session:Session= Depends(get_session)):
    delivery_man = session.exec(select(DeliveryBoy)).all()
    return delivery_man

