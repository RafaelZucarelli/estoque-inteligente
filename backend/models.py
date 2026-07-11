from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True)
    current_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=5)
    unit_cost = Column(Float, default=0.0)

    movements = relationship("StockMovement", back_populates="product")
    sales = relationship("Sale", back_populates="product")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    type = Column(String, nullable=False)  # "entrada", "saida", "ajuste"
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="movements")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sales")