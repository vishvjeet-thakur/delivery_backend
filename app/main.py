from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import admin, user, order, delivery_person, delivery
from app.db import init_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#LifeSpan event to initialise db before it start accepting request
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Delivery Management API",
    description="Backend for a Delivery API",
    version="1.0.0",
    lifespan=lifespan
)

#to allow cross origin communications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(admin.router, prefix="/admin", tags=["Admin"]) # For all the task like matching orders with deliveryboys, sending otps and verifying them etc
app.include_router(user.router, prefix="/user", tags=["User"]) # For user creation and authentication
app.include_router(order.router, prefix="/orders", tags=["Order"]) # For Order related end points
app.include_router(delivery_person.router, prefix="/deliveryboy", tags=["DeliveryBoy"]) #For  creating delivery boys  and other end points related to delivery boys
app.include_router(delivery.router, prefix="/delivery", tags=["Delivery"]) # For connecting order with deliveries
