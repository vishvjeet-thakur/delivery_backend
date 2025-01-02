from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.models.order import Order
from app.db import get_session

router = APIRouter()

@router.post("/") # creating new  user
def create_user(user: User, session: Session = Depends(get_session)): 
    session.add(user)
    session.commit()
    session.refresh(user)
    return user



@router.get("/{user_id}/orders/") #getting  all orders for a user
def view_user_orders(user_id: int, session: Session = Depends(get_session)):
    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders

@router.get('/') # getting all users
def view_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
