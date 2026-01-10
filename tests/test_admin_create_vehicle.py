from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_create_vehicle_missing_token_returns_401():
    r = client.post(
        "/admin/vehicles",
        json={"vehicle_type": "CAR", "plate_number": "PK0000AA", "model": "Test Model"},
    )
    assert r.status_code == 401

def test_admin_login_invalid_credentials_returns_401():
    r = client.post(
        "/auth/login",
        json={"email": "nope@urbango.com", "password": "wrong"},
    )
    assert r.status_code == 401
