from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import sys
import os
sys.path.append(os.path.abspath('../'))
from meeting_assistant_cli import summarize_and_translate

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": "This is a /item view"}

class Item(BaseModel):
    name: str
    price: float
    tags: list[str] = []

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/summarize/")
def generate_summary(text:str, language:str):
    return {"text": summarize_and_translate(text, language)}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="127.0.0.1")
