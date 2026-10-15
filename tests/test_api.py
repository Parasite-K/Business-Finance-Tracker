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

def test_create_project():
    response = client.post("/projects", json={
        "name": "Test Project",
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "estimated_revenue": 50000
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Project successfully created."


def test_get_nonexistent_project():
    response = client.get("/projects/999999")
    assert response.status_code == 404

def test_update_project():
    created = client.post("/projects", json={
        "name": "Project Before Update",
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "estimated_revenue": 50000
    })
    project_id = created.json()["project_id"]

    response = client.put(f"/projects/{project_id}", json={
        "name": "Project After Update",
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "estimated_revenue": 60000
    })

    assert response.status_code == 200


def test_delete_project():
    created = client.post("/projects", json={
        "name": "Project To Delete",
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "estimated_revenue": 50000
    })
    project_id = created.json()["project_id"]

    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 200

    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 404


def test_create_client():
    response = client.post("/clients", json={
        "name": "Test Client",
        "phone": "9876543210",
        "email": "test@example.com"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Client successfully created."


def test_get_nonexistent_client():
    response = client.get("/clients/999999")
    assert response.status_code == 404

def test_client_projects():
    client_response = client.post("/clients", json={
        "name": "Client With Project",
        "phone": "9876543210",
        "email": "projects@example.com"
    })
    client_id = client_response.json()["client_id"]

    project_response = client.post("/projects", json={
        "name": "Client Test Project",
        "client_id": client_id,
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "estimated_revenue": 50000
    })
    assert project_response.status_code == 200

    response = client.get(f"/clients/{client_id}/projects")

    assert response.status_code == 200
    assert response.json()["client_id"] == client_id
    assert len(response.json()["projects"]) == 1


##REPORTS TESTS
def test_financial_summary():
    response = client.get("/reports/summary")
    assert response.status_code == 200

    data = response.json()
    assert "total_income" in data
    assert "total_expense" in data


def test_monthly_report():
    response = client.get(
        "/reports/monthly",
        params={"year": 2026, "month": 10}
    )
    assert response.status_code == 200


def test_financial_summary_calculations():
    client.post("/transactions", json={
        "type": "income",
        "category": "Sales",
        "description": "Test report income",
        "date": "2026-10-15",
        "amount": 10000
    })

    client.post("/transactions", json={
        "type": "expense",
        "category": "Rent",
        "description": "Test report expense",
        "date": "2026-10-15",
        "amount": 3000
    })

    response = client.get("/reports/summary")
    assert response.status_code == 200

    data = response.json()
    print(data)


def test_create_project_invalid_dates():
    response = client.post("/projects", json={
        "name": "Invalid Project",
        "start_date": "2026-12-31",
        "end_date": "2026-10-01",
        "estimated_revenue": 50000
    })
    assert response.status_code == 422


def test_create_transaction_invalid_type():
    response = client.post("/transactions", json={
        "type": "refund",
        "category": "Rent",
        "description": "Invalid type",
        "date": "2026-10-15",
        "amount": 500
    })
    assert response.status_code == 422