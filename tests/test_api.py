from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_get_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

    assert data["limit"] == 20
    assert data["offset"] == 0
    assert isinstance(data["items"], list)

def test_transactions_with_limit():
    response = client.get("/transactions", params={"limit": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 5
    assert len(data["items"]) <= 5

def test_transactions_with_invalid_limit():
    response = client.get("/transactions", params={"limit": 0})
    assert response.status_code == 422

def test_transactions_with_large_offset():
    response = client.get("/transactions", params={"offset": 10000})
    assert response.status_code == 200
    data = response.json()
    assert not data["items"]
    assert data["offset"] == 10000

def test_create_transaction():
    response = client.post("/transactions", json= {
        "type": "expense",
        "category": "Rent",
        "description": "Test rent payment",
        "date": "2026-10-12",
        "amount": 5000
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction created successfully"

def test_create_transaction_negative_amount():
    response = client.post("/transactions", json={
        "type": "expense",
        "category": "Rent",
        "description": "Invalid transaction",
        "date": "2026-10-12",
        "amount": -500
    })
    assert response.status_code == 422


def test_create_transaction_invalid_category():
    response = client.post("/transactions", json={
        "type": "expense",
        "category": "Sales",
        "description": "Invalid category",
        "date": "2026-10-12",
        "amount": 500
    })
    assert response.status_code == 422

def test_get_transaction():
    create_response = client.post("/transactions", json={
        "type": "expense",
        "category": "Rent",
        "description": "Test retrieval",
        "date": "2026-10-12",
        "amount": 500
    })

    txn_id = create_response.json()["transaction_id"]

    response = client.get(f"/transactions/{txn_id}")

    assert response.status_code == 200
    assert response.json()["description"] == "Test retrieval"

def test_update_transaction():
    created = client.post("/transactions", json={
        "type": "expense",
        "category": "Rent",
        "description": "Before update",
        "date": "2026-10-12",
        "amount": 500
    })
    txn_id = created.json()["transaction_id"]

    response = client.put(f"/transactions/{txn_id}", json={
        "type": "expense",
        "category": "Rent",
        "description": "After update",
        "date": "2026-10-12",
        "amount": 700
    })

    assert response.status_code == 200
    assert response.json()["description"] == "After update"


def test_delete_transaction():
    created = client.post("/transactions", json={
        "type": "expense",
        "category": "Rent",
        "description": "To be deleted",
        "date": "2026-10-12",
        "amount": 500
    })
    txn_id = created.json()["transaction_id"]

    response = client.delete(f"/transactions/{txn_id}")
    assert response.status_code == 200

    response = client.get(f"/transactions/{txn_id}")
    assert response.status_code == 404