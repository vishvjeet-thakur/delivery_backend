from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import json
from typing import TYPE_CHECKING
from enum import Enum


# because of how FastApi is designed, to avoid cirular imports
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.delivery import Delivery
    from app.models.admin import Admin

class OrderStatus(str, Enum):
    CREATED = "Created"
    PICKED = "Picked"
    DELIVERED = "Delivered"
    ISSUE ="Issue"
    

# few attributes can be eliminated for better database performance .

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_items: str = Field(default=json.dumps(['dummy_item_1', 'dummy_item_2']))
    description: str = "dummy_order_description"
    amount: str = "dummy_order_amount"
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="orders") # one to one relationship
    admin_id: Optional[int] = Field(foreign_key="admin.id")
    admin: "Admin" = Relationship(back_populates="orders") # one to one relationship 
    delivery: "Delivery" = Relationship(back_populates="orders") #one to one relationship
    status: str = OrderStatus.CREATED  # status: created, assigned, in_delivery, delivered
