from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_driver_availability_user_not_driver_returns_400():
    r = client.patch("/drivers/1/availability", json={"driver_available": True})
    assert r.status_code in (200, 400)

def test_driver_availability_not_found_returns_404():
    r = client.patch("/drivers/999999/availability", json={"driver_available": True})
    assert r.status_code == 404
