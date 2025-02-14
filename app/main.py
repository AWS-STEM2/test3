from fastapi import FastAPI
from typing import List
from .schemas import Item

app = FastAPI()

# 임시 데이터 저장소
items = []

@app.post("/items/")
async def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < len(items):
        return items[item_id]
    return {"error": "Item not found"}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id < len(items):
        items[item_id] = item
        return item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id < len(items):
        deleted_item = items.pop(item_id)
        return deleted_item
    return {"error": "Item not found"}