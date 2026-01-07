# UrbanGo
## Vehicles

### GET /vehicles
Query params:
- `type` (optional): `CAR` | `SCOOTER` | `BIKE`

Responses:
- `200 OK` – returns available vehicles (optionally filtered by type)
- `400 Bad Request` – invalid `type` value

Examples:
- `/vehicles`
- `/vehicles?type=car`
## Bookings

### POST /bookings
Creates a new booking and atomically marks the vehicle as unavailable.

Request body:
- `rider_id` (int)
- `vehicle_id` (int)

Responses:
- `201 Created` – booking created
- `404 Not Found` – vehicle does not exist
- `409 Conflict` – vehicle already unavailable / already booked
- `422 Unprocessable Entity` – invalid payload
