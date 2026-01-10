BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    role VARCHAR(16) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    driver_available BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_users_role CHECK (role IN ('RIDER', 'DRIVER', 'ADMIN'))
);

CREATE TABLE IF NOT EXISTS vehicles (
    id BIGSERIAL PRIMARY KEY,
    vehicle_type VARCHAR(16) NOT NULL,
    plate_number VARCHAR(32) UNIQUE,
    model VARCHAR(80),
    status VARCHAR(16) NOT NULL DEFAULT 'AVAILABLE',
    available BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_vehicle_type CHECK (vehicle_type IN ('CAR', 'SCOOTER', 'BIKE')),
    CONSTRAINT chk_vehicle_status CHECK (status IN ('AVAILABLE', 'UNAVAILABLE', 'MAINTENANCE')),
    CONSTRAINT chk_vehicle_availability_consistency CHECK (
        (status = 'AVAILABLE' AND available = TRUE)
        OR (status <> 'AVAILABLE' AND available = FALSE)
    )
);

CREATE TABLE IF NOT EXISTS bookings (
    id BIGSERIAL PRIMARY KEY,
    rider_id BIGINT NOT NULL,
    driver_id BIGINT,
    vehicle_id BIGINT NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'REQUESTED',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    accepted_at TIMESTAMPTZ,
    ready_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    CONSTRAINT fk_bookings_rider FOREIGN KEY (rider_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_bookings_driver FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_bookings_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT,
    CONSTRAINT chk_booking_status CHECK (
        status IN ('REQUESTED', 'ACCEPTED', 'READY', 'COMPLETED', 'CANCELLED')
    )
);

CREATE TABLE IF NOT EXISTS booking_events_outbox (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT NOT NULL,
    event_type VARCHAR(32) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    CONSTRAINT fk_outbox_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS token_blacklist (
    id BIGSERIAL PRIMARY KEY,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_vehicles_type_available
    ON vehicles (vehicle_type, available);

CREATE INDEX IF NOT EXISTS idx_vehicles_status
    ON vehicles (status);

CREATE INDEX IF NOT EXISTS idx_bookings_rider_requested_at
    ON bookings (rider_id, requested_at DESC);

CREATE INDEX IF NOT EXISTS idx_bookings_status_requested_at
    ON bookings (status, requested_at DESC);

CREATE INDEX IF NOT EXISTS idx_bookings_vehicle_status
    ON bookings (vehicle_id, status);

CREATE INDEX IF NOT EXISTS idx_bookings_driver_accepted_at
    ON bookings (driver_id, accepted_at DESC);

CREATE INDEX IF NOT EXISTS idx_outbox_unprocessed
    ON booking_events_outbox (processed_at)
    WHERE processed_at IS NULL;

COMMIT;
