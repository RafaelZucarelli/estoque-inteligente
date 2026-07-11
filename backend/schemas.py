from pydantic import BaseModel
from typing import Optional


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