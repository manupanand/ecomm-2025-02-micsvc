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