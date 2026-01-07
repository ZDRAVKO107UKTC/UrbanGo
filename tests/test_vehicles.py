from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_vehicles_returns_200():
    r = client.get("/vehicles")
    assert r.status_code == 200

def test_get_vehicles_filter_by_type_returns_200():
    r = client.get("/vehicles?type=car")
    assert r.status_code == 200

def test_invalid_vehicle_type_returns_400():
    r = client.get("/vehicles?type=plane")
    assert r.status_code == 400
