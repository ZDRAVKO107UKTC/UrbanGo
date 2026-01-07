from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_vehicle_type_returns_400():
    r = client.get("/vehicles?type=plane")
    assert r.status_code == 400
