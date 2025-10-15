from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel, Field

class Data(BaseModel):
    x: int
    y: int

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello Data!"}

@app.post("/")
def calc(data:Data):
    z = data.x*data.y
    return {"result": z}

