from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.order import Order, OrderStatus
from app.db import get_session
from datetime import datetime


router = APIRouter()

@router.get("/") # to get all the orders placed till now
def get_all_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    return orders

@router.get("/{order_id}/") # to get orders by order_id
def get_order_details(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/place_order/") # to place new order
def place_order(order: Order, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@router.get("/user/{order_id}") # to get user corresponding to a user by user_id
def get_order_user(order_id:int, session:Session = Depends(get_session)):
    order = session.get(Order,order_id)
    user = order.user
    return user


@router.get("/orders_demo/not_delivered") # to get all the orders not delivered yet
def get_all_order_demo(sesssion:Session=Depends(get_session)):
    orders = sesssion.exec(select(Order).where(Order.status!=OrderStatus.DELIVERED)).all()
    demo_orders = []
    
    for order in orders:
        user = order.user
        delivery = order.delivery
        
        # Construct the demo_order dictionary for each order
        demo_order = {
            'customerName': user.name,
            'address': user.address,
            'amount': order.amount,
            'timeLeft': delivery.order_placed_at,  # Modify this as needed
            'billNumber': delivery.bill_number
        }
        
        # Append the demo_order to the list
        demo_orders.append(demo_order)
    
    return demo_orders

@router.get("/orders_demo/delivered") # to get all the orders delivered
def get_all_order_demo(sesssion:Session=Depends(get_session)):
    orders = sesssion.exec(select(Order).where(Order.status==OrderStatus.DELIVERED)).all()
    demo_orders = []
    
    for order in orders:
        user = order.user
        delivery = order.delivery
        
        # Construct the demo_order dictionary for each order
        demo_order = {
            'customerName': user.name,
            'address': user.address,
            'amount': order.amount,
            'timeLeft': delivery.completed_at,  # Modify this as needed
            'billNumber': delivery.bill_number
        }
        
        # Append the demo_order to the list
        demo_orders.append(demo_order)
    
    return demo_orders

@router.post('/amount/{order_id}/{amount}') # to update the amount of a order
def update_order_amount(order_id: int, amount: float, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404)
    order.amount=amount
    session.add(order)
    session.commit()
    session.refresh(order)
    return order