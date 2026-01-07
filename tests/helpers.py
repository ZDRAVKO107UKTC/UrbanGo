import os
from sqlalchemy import create_engine, text

def reset_for_vehicle(vehicle_id: int) -> None:
    url = "postgresql+psycopg://postgres:123@localhost:5432/urbango"
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    engine = create_engine(url, pool_pre_ping=True)
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM bookings WHERE vehicle_id = :vid"), {"vid": vehicle_id})
        conn.execute(text("UPDATE vehicles SET status='AVAILABLE', available=true WHERE id = :vid"), {"vid": vehicle_id})
