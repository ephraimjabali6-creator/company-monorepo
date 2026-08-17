from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Product API - scaffold")

class Product(BaseModel):
    id: int
    name: str
    description: str = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/product")
def create_product(p: Product):
    # Placeholder: persist to DB in real implementation
    return {"created": True, "product": p.dict()}
