from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_amount: float

ORDERS = []
NEXT_ID = 1

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders")
def create_order(items: List[OrderItem]):
    global NEXT_ID
    total = 0.0
    # For simplicity, assume each product costs 100
    for item in items:
        total += item.quantity * 100

    order = Order(id=NEXT_ID, items=items, total_amount=total)
    ORDERS.append(order)
    NEXT_ID += 1
    return order

@app.get("/orders")
def list_orders():
    return ORDERS
