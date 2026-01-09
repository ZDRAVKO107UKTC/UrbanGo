from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rider_history_rider_not_found_returns_404():
    r = client.get("/riders/999999/bookings")
    assert r.status_code == 404
