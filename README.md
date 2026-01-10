# UrbanGo Backend

UrbanGo is a ride-sharing backend platform supporting Riders, Drivers, and Admins.
The system is designed with clean architecture principles, transactional safety, and role-based access control.

---

## Tech Stack

- **Python 3.11**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **JWT (jose)**
- **Pytest**
- **Uvicorn**

---

## Architecture Overview

- Monolithic REST API
- Repository pattern for data access
- Dependency Injection via FastAPI
- ACID transactions for booking flow
- Row-level locking to prevent double bookings
- Observer pattern for booking state events
- Soft deletes for vehicles (status-based)

---

## Authentication & Authorization

UrbanGo uses JWT-based authentication with role claims.

**Supported roles:**
- `RIDER`
- `DRIVER`
- `ADMIN`

All protected endpoints require a valid Bearer token.

### POST `/auth/login`

Authenticates a user and returns a JWT access token.

**Request body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Responses:**
- `200 OK` – returns `access_token` and `token_type`
- `401 Unauthorized` – invalid credentials

**Security notes:**
- Passwords are hashed (bcrypt)
- JWT expires after 60 minutes
- Token contains `sub` (user ID) and `role`

### POST `/auth/logout`

Logs out the authenticated user by revoking the current JWT token.

**Authorization:**
```
Authorization: Bearer <token>
```

**Responses:**
- `204 No Content`
- `401 Unauthorized` – invalid or revoked token

**Implementation note:**
JWT tokens are stateless; logout is implemented via a token blacklist table checked on every protected request.

---

## Admin Endpoints

### POST `/admin/vehicles`

Creates a new vehicle. **ADMIN only.**

**Request body:**
```json
{
  "vehicle_type": "CAR | SCOOTER | BIKE",
  "plate_number": "string (optional)",
  "model": "string"
}
```

**Responses:**
- `201 Created`
- `401 Unauthorized`
- `403 Forbidden`

### GET `/admin/bookings`

Lists all bookings. **ADMIN only.**

**Query params:**
- `status` (optional): `REQUESTED | ACCEPTED | READY | COMPLETED`

**Responses:**
- `200 OK`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`

### PATCH `/admin/vehicles/{vehicle_id}/disable`

Soft-disables a vehicle. **ADMIN only.**

**Behavior:**
- Sets `status = UNAVAILABLE`
- Sets `available = false`

This respects database constraints:
- `AVAILABLE` → `available = true`
- `UNAVAILABLE / MAINTENANCE` → `available = false`

**Responses:**
- `200 OK`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict` (already disabled)

---

## Vehicles

### GET `/vehicles`

Returns available vehicles.

**Query params:**
- `type` (optional): `CAR | SCOOTER | BIKE`

**Responses:**
- `200 OK`
- `400 Bad Request` – invalid type

**Examples:**
- `/vehicles`
- `/vehicles?type=car`

---

## Bookings

### POST `/bookings`

Creates a new booking and atomically marks the vehicle unavailable.

**Request body:**
```json
{
  "rider_id": "int",
  "vehicle_id": "int"
}
```

**Transactional guarantees:**
- Uses SQL transaction
- Uses `SELECT … FOR UPDATE`
- Prevents double booking (US-12)

**Responses:**
- `201 Created`
- `404 Not Found` – vehicle not found
- `409 Conflict` – vehicle unavailable
- `422 Unprocessable Entity` – invalid payload

### GET `/bookings/{booking_id}?rider_id={rider_id}`

Returns booking details for a rider.

**Responses:**
- `200 OK`
- `403 Forbidden` – booking does not belong to rider
- `404 Not Found`

### PATCH `/bookings/{booking_id}/complete?driver_id={driver_id}`

Marks a `READY` booking as `COMPLETED`.

**Responses:**
- `200 OK`
- `404 Not Found`
- `400 Bad Request` – user not a DRIVER
- `403 Forbidden` – not assigned driver
- `409 Conflict` – booking must be READY

---

## Drivers

### PATCH `/drivers/{driver_id}/availability`

Updates driver availability.

**Request body:**
```json
{
  "driver_available": "bool"
}
```

**Responses:**
- `200 OK`
- `404 Not Found`
- `400 Bad Request` – user is not a DRIVER

### PATCH `/bookings/{booking_id}/accept?driver_id={driver_id}`

Accepts a `REQUESTED` booking.

**Responses:**
- `200 OK`
- `404 Not Found`
- `400 Bad Request` – invalid driver
- `409 Conflict` – booking not REQUESTED

### GET `/bookings/pending?driver_id={driver_id}`

Returns all pending ride requests (`REQUESTED` state). **DRIVER only.**

**Responses:**
- `200 OK`
- `404 Not Found` – driver not found
- `400 Bad Request` – user not a DRIVER

### PATCH `/bookings/{booking_id}/ready`

Marks an `ACCEPTED` booking as `READY`.

**Side effects (Observer Pattern):**
- Emits `BOOKING_READY` event
- Triggers `NotificationService`
- Triggers `BillingService`
- Writes to `booking_events_outbox`

**Responses:**
- `200 OK`
- `404 Not Found`
- `409 Conflict` – booking must be ACCEPTED

---

## Riders

### GET `/riders/{rider_id}/bookings`

Returns rider booking history (newest first).

**Responses:**
- `200 OK`
- `404 Not Found`

---

## Testing

Run all tests:

```bash
pytest -q
```

**Includes:**
- Concurrency test for double booking (US-12)
- Role enforcement tests
- Admin restrictions
- Transaction rollback validation

---

## Design Principles Applied

### SOLID
- Single Responsibility (routes vs services vs repositories)
- Dependency Inversion (interfaces & DI)

### ACID Transactions
- Row-level locking
- Soft deletes
- Event-driven side effects

---

## Project Status

 **All User Stories implemented and completed.**
System is production-safe by design and review-ready.
