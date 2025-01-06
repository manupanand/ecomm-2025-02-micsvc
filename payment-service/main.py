from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from dotenv import load_dotenv,find_dotenv
from starlette.requests import Request
import requests
import os
import uvicorn
# Intitialize Fast api app
app:FastAPI=FastAPI()
#load environment variable from .env
load_dotenv(find_dotenv())
#get redis url from environment
redis_url=os.getenv("REDIS") # this should be different database
#Create synchronous redis connection for redis-om

try:
    
    redis = get_redis_connection(url=redis_url)
except Exception as error:
    print(f"Error connecting to Redis: {error}")
#add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],#allow frontent to interact
    allow_methods=['*'],
    allow_headers=['*']
)
#define structure of an order
class OrderBase(BaseModel):
    product_id:str
    price:float
    delivery_charge:float
    total:float
    quantity:int
    status:str#pending, completed, refunded

class Order(HashModel,OrderBase):

    class Meta:
        database=redis


@app.post('/orders')
async def create_order(request:Request): #id and quantity we get it from inventory using request
    body= await request.json()
    #send request to microsercvice inventory
    req= requests.get('http://localhost:3500/product/%s' % body['id'])# microservice calling internally change this to grpc
    product= req.json()
    order = Order(
        product_id=body['id'],
        price=product['price']*body['quantity'],
        delivery_charge=0.2*product['price'],
        total=1.2*product['price']*body['quantity'],
        quantity=body['quantity'],
        status="pending"
    )
    order.save()
    order_completed(order)

    return order

def order_completed(order:Order):
    order.status="completed"
    order.save()





if __name__== "__main__":
    uvicorn.run("main:app")