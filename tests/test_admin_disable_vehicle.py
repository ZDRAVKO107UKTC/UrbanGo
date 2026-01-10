from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_disable_vehicle_without_token_returns_401():
    r = client.patch("/admin/vehicles/1/disable")
    assert r.status_code == 401
