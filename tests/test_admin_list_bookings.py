from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_list_bookings_without_token_returns_401():
    r = client.get("/admin/bookings")
    assert r.status_code == 401
