from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_complete_booking_not_found_returns_404():
    r = client.patch("/bookings/999999/complete?driver_id=2")
    assert r.status_code == 404
