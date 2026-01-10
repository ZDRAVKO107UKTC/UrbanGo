# UrbanGo

## Authentication

### POST /auth/login
Authenticates a user and returns a JWT access token.

Request body:
- `email` (string, email format)
- `password` (string)

Responses:
- `200 OK` – returns `access_token` and `token_type` (bearer)
- `401 Unauthorized` – invalid credentials

Security:
- Passwords are hashed using SHA256 + bcrypt
- JWT tokens expire after 60 minutes
- Tokens include user ID (`sub`) and role claims
### POST /auth/logout
Logs out the authenticated user by revoking the current JWT token.

Authorization:
- Bearer Token

Responses:
- 204 No Content
- 401 Unauthorized (invalid or revoked token)

## Admin

### POST /admin/vehicles
Creates a new vehicle in the system. Requires ADMIN role.

Request body:
- `vehicle_type` (string)
- `plate_number` (string, optional)
- `model` (string)

Headers:
- `Authorization: Bearer <token>` (ADMIN role required)

Responses:
- `201 Created` – vehicle created successfully
- `401 Unauthorized` – missing or invalid token
- `403 Forbidden` – user is not an ADMIN
### GET /admin/bookings
Lists all bookings (admin-only). Supports optional status filter.

Query:
- status (optional): REQUESTED | ACCEPTED | READY | COMPLETED

Responses:
- 200 OK
- 400 Bad Request (invalid status)
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (not an admin)
### PATCH /admin/vehicles/{vehicle_id}/disable
Disables a vehicle (soft delete)

Authorization:
- Bearer Token (ADMIN)

Behavior:
- Sets available = false
- Sets status = DISABLED

Responses:
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict (already disabled)


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
- ### GET /bookings/{booking_id}?rider_id={rider_id}
Returns booking details for a rider.

Responses:
- 200 OK – booking details
- 404 Not Found – booking not found
- 403 Forbidden – booking does not belong to rider

### PATCH /bookings/{booking_id}/complete?driver_id={driver_id}
Marks a READY booking as COMPLETED.

Responses:
- 200 OK – booking completed
- 404 Not Found – booking or driver not found
- 400 Bad Request – user is not a DRIVER
- 403 Forbidden – booking not assigned to driver
- 409 Conflict – booking must be READY before COMPLETED
### GET /bookings/pending?driver_id={driver_id}
Returns all pending ride requests (bookings in REQUESTED state). Driver-only.

Responses:
- 200 OK – list of pending bookings
- 404 Not Found – driver not found
- 400 Bad Request – user exists but is not a DRIVER
