from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.admin import Admin
from app.models.order import Order
from app.db import get_session
from app.models.delivery import Delivery
from app.models.delivery_partner import DeliveryBoy, DeliveryStatus
from app.models.order import OrderStatus
import random
from datetime import datetime, timezone




router = APIRouter()

@router.post("/") # to make a admin
def create_admin(admin: Admin, session: Session = Depends(get_session)):
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin

@router.get("/orders/") # to  get all orders
def get_all_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    return orders

@router.post("/assign-delivery/{order_id}/{delivery_boy_id}") # to assign a delivery of a order to a delivery boy
def assign_delivery(order_id: int, delivery_boy_id: int, session: Session = Depends(get_session)):
    otp = str(random.randint(10000,99999))
    delivery =Delivery(order_id=order_id,delivery_boy_id=delivery_boy_id,otp=otp,order_placed_at=datetime.now())
    order = session.get(Order, order_id)
    delivery_boy = session.get(DeliveryBoy,delivery_boy_id)
    if not order or not delivery_boy:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "assigned"
    delivery_boy.status = DeliveryStatus.IN_DELIVERY
    session.add(order)
    session.add(delivery)
    session.add(delivery_boy)
    session.commit()
    return {"message": f"Delivery Boy {delivery_boy_id} assigned to Order {order_id}"}


@router.post('/order_picked/{delivery_id}/{bill_number}') #  to mark a order picked- when delivery boy collects the order from  the store or warehouse
def order_picked(delivery_id:int,bill_number:str, session:Session= Depends(get_session)):
    delivery=session.get(Delivery,delivery_id)
    order = delivery.orders
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    if not delivery:
        raise HTTPException(status_code=404,detail="Order never assigned to a delivery boy")
    order.status = OrderStatus.PICKED
    delivery.bill_number = bill_number
    session.add(order)
    session.add(delivery)
    session.commit()
    session.refresh(delivery)
    session.refresh(order)
    return delivery,order

# while giving the delivery to the customer upload the link of photo of the delivery item - Just in case 
@router.post('/order_delivered/{order_id}/{delivery_photo}') 
def order_delivered(order_id:int,delivery_photo:str, session:Session=Depends(get_session)):
    order = session.get(Order,order_id)
    if not order:
        raise HTTPException(status_code=404, details="order not found")
    order.status = OrderStatus.DELIVERED
    delivery = order.delivery
    delivery.completed_at =datetime.now()
    delivery.delivery_photo= delivery_photo
    delivery_boy = delivery.delivery_boy
    delivery_boy.status = DeliveryStatus.AVAILABLE

    session.add(delivery)
    session.add(delivery_boy)
    session.add(order)
    session.commit()
    session.refresh(order)
    session.refresh(delivery)
    session.refresh(delivery_boy)

    return order, delivery, delivery_boy


 # to verifying the otp , which was generated at the time a delivery boy was assigned to the delivery , if verified ,it will be set to delivered
@router.get('/verify_otp/{otp}/{bill_number}') 
def verify_otp(otp:str,bill_number:str, session:Session =Depends(get_session)):
    delivery = session.exec(select(Delivery).where(Delivery.bill_number==bill_number)).one()
    order= delivery.orders
    if not delivery:
        raise HTTPException(status_code=404,detail="Order not found")
    verified=False
    if delivery.otp == otp:
        verified=True
        delivery.completed_at = datetime.now()
        order.status = OrderStatus.DELIVERED
        session.add(delivery)
        session.add(order)
        session.commit()
    return {verified:verified}
    



