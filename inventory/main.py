from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from dotenv import load_dotenv,find_dotenv
import os
# Intitialize Fast api app
app:FastAPI=FastAPI()
#load environment variable from .env
load_dotenv(find_dotenv())
#get redis url from environment
redis_url=os.getenv("REDIS")
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
#Define product model with redis-om
class ProductBase(BaseModel):
    name: str
    price:float
    quantity:int

class Product(HashModel,ProductBase):
    
    class Meta:
        database=redis#use synchronous redis connection
    



#define root endpoint
@app.get("/")
async def root():
    return {"message":"got main"}
#fetch all products  primary keys
@app.get('/products')
async def all():
    return Product.all_pks()# return all primary keys
#define post endpoint to  create  a new product
@app.post('/products')
def create(product:ProductBase):
    product_redis=Product(**product.dict())#save product in redis have to convert it to redis type 15.26
    return {"message": "Product created", "product": product_redis.dict()}