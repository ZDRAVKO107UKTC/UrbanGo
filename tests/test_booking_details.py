from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_booking_details_not_found_returns_404():
    r = client.get("/bookings/999999?rider_id=1")
    assert r.status_code == 404
