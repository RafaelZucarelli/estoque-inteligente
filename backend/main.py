from fastapi import FastAPI
from database import engine, Base
import models
from routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Estoque Inteligente API")

app.include_router(products.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}