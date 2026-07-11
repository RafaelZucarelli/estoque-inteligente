from fastapi import FastAPI

app = FastAPI(title="Estoque Inteligente API")

@app.get("/health")
def health_check():
    return {"status": "ok"}