import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

db_engine = None
SessionLocal = None

surge_cache: Dict[str, Dict[str, Any]] = {}

CACHE_TTL_SECONDS = 10  # Cache validity duration


def initialize_database():
    global db_engine, SessionLocal

    if db_engine is None:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set")

        db_engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
        SessionLocal = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)

        metadata = MetaData()
        Table('incidents', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('region_id', String, nullable=False),
              Column('multiplier', Float, nullable=False),
              Column('calculated_at', String, nullable=False)
              )
        metadata.create_all(db_engine)

def calculate_surge_multiplier(rider_count: int, active_driver_count: int) -> float:
    if active_driver_count == 0:
        return 3.0

    ratio = rider_count / active_driver_count

    multiplier = 1.0 + (ratio / 2.0) * 0.5

    return min(multiplier, 4.0)


def persist_surge_calculation(region_id: str, multiplier: float, timestamp: str) -> None:
    initialize_database()
    db: Session = SessionLocal()
    try:
        db.execute(
            text("INSERT INTO incidents (region_id, multiplier, calculated_at) VALUES (:region_id, :multiplier, :calculated_at)"),
            {"region_id": region_id, "multiplier": multiplier, "calculated_at": timestamp}
        )
        db.commit()
    finally:
        db.close()


def check_cache(region_id: str) -> Optional[float]:
    if region_id in surge_cache:
        cached_data = surge_cache[region_id]
        age = time.time() - cached_data["timestamp"]

        if age < CACHE_TTL_SECONDS:
            return cached_data["multiplier"]
        else:
            del surge_cache[region_id]

    return None


def update_cache(region_id: str, multiplier: float) -> None:
    surge_cache[region_id] = {
        "multiplier": multiplier,
        "timestamp": time.time()
    }


def lambda_handler(event: Any, context: Any = None) -> Dict[str, Any]:
    if not isinstance(event, dict):
        return {
            "status": 422,
            "error": "Unprocessable Entity",
            "message": "Event must be a dictionary"
        }

    region_id = event.get("region_id")
    if not region_id:
        return {
            "status": 422,
            "error": "Unprocessable Entity",
            "message": "Missing required field: region_id"
        }


    cached_multiplier = check_cache(region_id)
    if cached_multiplier is not None:
        return {
            "region_id": region_id,
            "multiplier": cached_multiplier,
            "source": "cache"
        }

    try:
        rider_count = int(event.get("rider_count", 0))
        active_driver_count = int(event.get("active_driver_count", 0))
        timestamp = event.get("timestamp", datetime.now(timezone.utc).isoformat())

        multiplier = calculate_surge_multiplier(rider_count, active_driver_count)

        persist_surge_calculation(region_id, multiplier, timestamp)

        update_cache(region_id, multiplier)

        return {
            "region_id": region_id,
            "multiplier": multiplier,
            "source": "compute"
        }

    except (ValueError, TypeError) as e:
        return {
            "status": 422,
            "error": "Unprocessable Entity",
            "message": f"Invalid input data: {str(e)}"
        }
    except Exception as e:
        return {
            "status": 500,
            "error": "Internal Server Error",
            "message": f"Unexpected error: {str(e)}"
        }


if __name__ == "__main__":
    test_events = [
        {
            "region_id": "downtown_sf",
            "rider_count": 100,
            "active_driver_count": 25,
            "timestamp": "2026-03-04T18:00:00Z"
        },
        {
            "region_id": "downtown_sf",  # Should hit cache
            "rider_count": 100,
            "active_driver_count": 25,
            "timestamp": "2026-03-04T18:00:05Z"
        },
        {
            "region_id": "airport",
            "rider_count": 50,
            "active_driver_count": 0,  # Zero-driver test
            "timestamp": "2026-03-04T18:00:00Z"
        },
        {
            "region_id": "mission_district",
            "rider_count": 200,
            "active_driver_count": 10,  # High surge test
            "timestamp": "2026-03-04T18:00:00Z"
        }
    ]

    print("=== UrbanGo Dynamic Surge Engine - Test Run ===\n")
    for i, event in enumerate(test_events, 1):
        result = lambda_handler(event)
        print(f"Test {i}: {result}")
        if i == 1:
            time.sleep(1)  # Brief pause to demonstrate cache hit on test 2

    print("\n=== Cache warm-start demonstration ===")
    time.sleep(11)  # Wait for cache to expire
    result = lambda_handler(test_events[0])
    print(f"After cache expiry: {result}")
