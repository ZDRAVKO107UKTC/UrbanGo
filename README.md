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
## Drivers

### PATCH /drivers/{driver_id}/availability
Request body:
- `driver_available` (bool)

Responses:
- `200 OK` – updated availability
- `404 Not Found` – driver not found
- `400 Bad Request` – user exists but is not a DRIVER
### PATCH /bookings/{booking_id}/accept?driver_id={driver_id}
Accepts a REQUESTED booking.

Responses:
- 200 OK – booking accepted
- 404 Not Found – booking or driver not found
- 400 Bad Request – driver invalid role or not available
- 409 Conflict – booking not in REQUESTED state
### PATCH /bookings/{booking_id}/ready
Marks an ACCEPTED booking as READY. Emits a BOOKING_READY event.

Responses:
- 200 OK – booking marked READY
- 404 Not Found – booking not found
- 409 Conflict – booking must be ACCEPTED before READY

Observer Pattern:
When a booking becomes READY, NotificationService and BillingService are triggered via an in-process EventBus.
An outbox record is also written to `booking_events_outbox` for reliability and future async processing.
## Riders

### GET /riders/{rider_id}/bookings
Returns booking history for a rider ordered by newest first.

Responses:
- 200 OK – list of bookings (may be empty)
- 404 Not Found – rider not found
