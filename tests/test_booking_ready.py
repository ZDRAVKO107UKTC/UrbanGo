from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_mark_ready_booking_not_found_returns_404():
    r = client.patch("/bookings/999999/ready")
    assert r.status_code == 404
