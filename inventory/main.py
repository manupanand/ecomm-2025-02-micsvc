from fastapi import FastAPI

from dotenv import load_dotenv,find_dotenv
import os

load_dotenv(find_dotenv())
redis_url=os.getenv("REDIS")
print(redis_url)

app:FastAPI=FastAPI()

@app.get("/")
def get_main():
    return {"message":"got main"}