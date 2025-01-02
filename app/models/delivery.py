from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.order import Order
from datetime import datetime,timezone
from app.models.delivery_partner import DeliveryBoy

class Delivery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id:int = Field(foreign_key='order.id')
    orders: Order = Relationship(back_populates="delivery")
    delivery_boy_id: Optional[int] = Field(default=None,foreign_key="deliveryboy.id")
    delivery_boy:DeliveryBoy = Relationship(back_populates="delivery")
    otp:str ="dummy_otp"
    delivery_photo: Optional[str] = None 
    bill_number:str="dummy_bill"
    completed_at:datetime|None = Field(default=None)
    order_placed_at:datetime|None =Field(default=None)
