from forecasting import calculate_forecast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU já cadastrado")

    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()
    return {"message": "Produto removido com sucesso"}

@router.post("/{product_id}/sale", response_model=schemas.SaleResponse)
def register_sale(product_id: int, sale_data: schemas.SaleCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if sale_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    if product.current_stock < sale_data.quantity:
        raise HTTPException(status_code=400, detail="Estoque insuficiente para essa venda")

    # Registra a venda
    new_sale = models.Sale(product_id=product_id, quantity=sale_data.quantity)
    db.add(new_sale)

    # Registra a movimentação de saída (auditoria)
    movement = models.StockMovement(
        product_id=product_id,
        type="saida",
        quantity=sale_data.quantity
    )
    db.add(movement)

    # Atualiza o estoque atual
    product.current_stock -= sale_data.quantity

    db.commit()
    db.refresh(new_sale)
    return new_sale


@router.post("/{product_id}/restock", response_model=schemas.StockMovementResponse)
def register_restock(product_id: int, restock_data: schemas.RestockCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if restock_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    movement = models.StockMovement(
        product_id=product_id,
        type="entrada",
        quantity=restock_data.quantity
    )
    db.add(movement)

    product.current_stock += restock_data.quantity

    db.commit()
    db.refresh(movement)
    return movement

@router.get("/{product_id}/forecast", response_model=schemas.ForecastResponse)
def get_forecast(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    forecast_data = calculate_forecast(product, db)

    return schemas.ForecastResponse(
        product_id=product.id,
        product_name=product.name,
        current_stock=product.current_stock,
        **forecast_data
    )