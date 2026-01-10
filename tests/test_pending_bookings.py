from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pending_bookings_driver_not_found_returns_404():
    r = client.get("/bookings/pending?driver_id=999999")
    assert r.status_code == 404
