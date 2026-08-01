from fastapi import FastAPI
app=FastAPI()
# In-memory database
PRODUCTS=[
    {"id":1,"name":"Laptop","price":1200},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Keyboard", "price": 80},
]

@app.get("/health")
def health():
        return{"status":"ok"}

@app.get("/products")
def list_products():
        return  PRODUCTS

@app.get("/products/{product_id}")
def get_product(product_id:int):
        for p in PRODUCTS:
                if p["id"]==product_id:
                    return p
        return{"error":"Product not found"}
        
        