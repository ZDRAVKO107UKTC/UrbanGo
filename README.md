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
