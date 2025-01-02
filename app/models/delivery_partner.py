from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Literal, List
# from app.models.order import Order.
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.delivery import Delivery


class DeliveryStatus(str, Enum):
    AVAILABLE = "available"
    AT_STORE = "at_store"
    INACTIVE = "inactive"
    IN_DELIVERY = "in_delivery"

class DeliveryBoy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "dummy_name_delivery_person"
    email: str = "dummy_email_delivery_person"
    password: str = "dummy_password_delivery_person"
    status: DeliveryStatus = DeliveryStatus.INACTIVE
    delivery: List['Delivery']|None = Relationship(back_populates="delivery_boy")
