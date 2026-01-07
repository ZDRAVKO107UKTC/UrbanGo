import asyncio
import httpx
from tests.helpers import reset_for_vehicle

BASE_URL = "http://127.0.0.1:8000"

async def _post_booking(client: httpx.AsyncClient, rider_id: int, vehicle_id: int) -> int:
    r = await client.post(
        f"{BASE_URL}/bookings",
        json={"rider_id": rider_id, "vehicle_id": vehicle_id},
    )
    return r.status_code

def test_concurrent_booking_same_vehicle_one_wins():
    vehicle_id = 1
    rider_id = 1

    reset_for_vehicle(vehicle_id)

    async def run():
        async with httpx.AsyncClient(timeout=10.0) as client:
            return await asyncio.gather(
                _post_booking(client, rider_id, vehicle_id),
                _post_booking(client, rider_id, vehicle_id),
            )

    results = asyncio.run(run())
    assert sorted(results) == [201, 409]
