def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Feijão 1kg",
        "sku": "FEJ-001",
        "current_stock": 20,
        "reorder_point": 5,
        "unit_cost": 8.50
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Feijão 1kg"
    assert data["sku"] == "FEJ-001"
    assert "id" in data


def test_create_product_duplicate_sku(client):
    client.post("/products/", json={
        "name": "Feijão 1kg", "sku": "FEJ-001", "current_stock": 20
    })
    response = client.post("/products/", json={
        "name": "Feijão 2kg", "sku": "FEJ-001", "current_stock": 10
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "SKU já cadastrado"


def test_list_products(client):
    client.post("/products/", json={"name": "Produto A", "sku": "A-001"})
    client.post("/products/", json={"name": "Produto B", "sku": "B-001"})

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_register_sale_decreases_stock(client):
    create_response = client.post("/products/", json={
        "name": "Arroz 5kg", "sku": "ARZ-001", "current_stock": 50
    })
    product_id = create_response.json()["id"]

    sale_response = client.post(f"/products/{product_id}/sale", json={"quantity": 10})
    assert sale_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")
    assert product_response.json()["current_stock"] == 40


def test_register_sale_insufficient_stock(client):
    create_response = client.post("/products/", json={
        "name": "Arroz 5kg", "sku": "ARZ-001", "current_stock": 5
    })
    product_id = create_response.json()["id"]

    sale_response = client.post(f"/products/{product_id}/sale", json={"quantity": 10})
    assert sale_response.status_code == 400
    assert sale_response.json()["detail"] == "Estoque insuficiente para essa venda"


def test_register_restock_increases_stock(client):
    create_response = client.post("/products/", json={
        "name": "Arroz 5kg", "sku": "ARZ-001", "current_stock": 10
    })
    product_id = create_response.json()["id"]

    restock_response = client.post(f"/products/{product_id}/restock", json={"quantity": 20})
    assert restock_response.status_code == 200

    product_response = client.get(f"/products/{product_id}")
    assert product_response.json()["current_stock"] == 30
