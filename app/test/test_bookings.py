from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_booking_vehicle_not_found_returns_404():
    r = client.post("/bookings", json={"rider_id": 1, "vehicle_id": 999999})
    assert r.status_code == 404

def test_create_booking_invalid_payload_returns_422():
    r = client.post("/bookings", json={"rider_id": 0, "vehicle_id": 1})
    assert r.status_code == 422
