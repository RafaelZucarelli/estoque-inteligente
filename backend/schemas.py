from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    sku: str
    current_stock: int = 0
    reorder_point: int = 5
    unit_cost: float = 0.0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    current_stock: Optional[int] = None
    reorder_point: Optional[int] = None
    unit_cost: Optional[float] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class SaleCreate(BaseModel):
    quantity: int


class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    date: datetime

    class Config:
        from_attributes = True


class RestockCreate(BaseModel):
    quantity: int


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    type: str
    quantity: int
    date: datetime

    class Config:
        from_attributes = True


class ForecastResponse(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    average_daily_sales: float
    days_until_stockout: Optional[float]
    status: str

class ProductWithForecast(BaseModel):
    id: int
    name: str
    sku: str
    current_stock: int
    reorder_point: int
    unit_cost: float
    average_daily_sales: float
    days_until_stockout: Optional[float]
    status: str
