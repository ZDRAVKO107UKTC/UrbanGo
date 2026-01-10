from fastapi import FastAPI

from app.core.events import EventBus
from app.services.notification_service import NotificationService
from app.services.billing_service import BillingService

from app.models import vehicle  # noqa: F401
from app.models import booking  # noqa: F401
from app.models import user     # noqa: F401
from app.models import outbox   # noqa: F401

from app.api.routes.vehicles import router as vehicles_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.drivers import router as drivers_router
from app.api.routes.booking_accept import router as booking_accept_router
from app.api.routes.booking_status import router as booking_status_router
from app.api.routes.riders import router as riders_router
from app.api.routes.booking_details import router as booking_details_router
from app.api.routes.booking_complete import router as booking_complete_router




app = FastAPI(title="UrbanGo API")

event_bus = EventBus()
notification_service = NotificationService()
billing_service = BillingService()

event_bus.subscribe("BOOKING_READY", notification_service.on_booking_ready)
event_bus.subscribe("BOOKING_READY", billing_service.on_booking_ready)

app.include_router(vehicles_router)
app.include_router(bookings_router)
app.include_router(drivers_router)
app.include_router(booking_accept_router)
app.include_router(booking_status_router)
app.include_router(riders_router)
app.include_router(booking_details_router)
app.include_router(booking_complete_router)


