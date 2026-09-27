from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_register_login_and_crud():
    username = "testuser"
    r = client.post("/auth/register", json={"username": username, "password": "Password123!"})
    assert r.status_code == 201

    r = client.post("/auth/login", json={"username": username, "password": "Password123!"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/employees", headers=headers, json={
        "name": "John Doe",
        "email": "john@example.com",
        "department": "IT",
        "designation": "Developer"
    })
    assert r.status_code == 201
    employee_id = r.json()["id"]

    assert client.get("/employees", headers=headers).status_code == 200
    assert client.get(f"/employees/{employee_id}", headers=headers).status_code == 200

    r = client.put(f"/employees/{employee_id}", headers=headers, json={
        "name": "John Updated",
        "email": "john@example.com",
        "department": "IT",
        "designation": "Senior Developer"
    })
    assert r.status_code == 200
    assert client.delete(f"/employees/{employee_id}", headers=headers).status_code == 200
