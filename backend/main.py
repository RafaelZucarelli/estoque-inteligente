from fastapi import FastAPI
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Estoque Inteligente API")

@app.get("/health")
def health_check():
    return {"status": "ok"}