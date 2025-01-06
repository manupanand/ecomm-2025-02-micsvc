from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from dotenv import load_dotenv,find_dotenv
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







if __name__== "__main__":
    uvicorn.run("main:app")