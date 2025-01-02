from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.order import Order



# a model for User - basic details but more details can be added
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "Dummy_name" # default name
    email: str = "Dummy_email" #default email
    password: str = "Dummy_password" # default password - for testing and demo purposes
    address: str = "Dummy_address" # defaultl address
    orders: List[Order]= Relationship(back_populates="user") # one to many relationship to user
