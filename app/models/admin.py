from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.order import Order


class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "dummy_name_admin"
    email: str = "dummy_email_admin"
    password: str = "dummy_password_admin"
    orders: List["Order"] = Relationship(back_populates="admin")
