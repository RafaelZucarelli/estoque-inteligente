from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from routers import products
from forecasting import calculate_forecast

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Estoque Inteligente API")

app.include_router(products.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    alerts = []

    for product in all_products:
        forecast_data = calculate_forecast(product, db)

        if forecast_data["status"] in ["critico", "atencao"]:
            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "current_stock": product.current_stock,
                **forecast_data
            })

    return {"total_alerts": len(alerts), "alerts": alerts}