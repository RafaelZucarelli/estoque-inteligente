from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import models


def calculate_forecast(product: models.Product, db: Session, days_window: int = 30):
    cutoff_date = datetime.utcnow() - timedelta(days=days_window)

    total_sold = (
        db.query(models.Sale)
        .filter(models.Sale.product_id == product.id)
        .filter(models.Sale.date >= cutoff_date)
        .all()
    )

    total_quantity = sum(sale.quantity for sale in total_sold)

    if total_quantity == 0:
        return {
            "average_daily_sales": 0.0,
            "days_until_stockout": None,
            "status": "sem_dados"
        }

    average_daily_sales = total_quantity / days_window

    if product.current_stock == 0:
        return {
            "average_daily_sales": round(average_daily_sales, 2),
            "days_until_stockout": 0,
            "status": "critico"
        }

    days_until_stockout = product.current_stock / average_daily_sales

    if days_until_stockout <= 7:
        status = "critico"
    elif days_until_stockout <= 15:
        status = "atencao"
    else:
        status = "ok"

    return {
        "average_daily_sales": round(average_daily_sales, 2),
        "days_until_stockout": round(days_until_stockout, 1),
        "status": status
    }