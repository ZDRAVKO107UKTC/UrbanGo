from fastapi import FastAPI

from app.models import vehicle  # noqa: F401
from app.models import booking  # noqa: F401
from app.models import user     # noqa: F401



from app.api.routes.vehicles import router as vehicles_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.drivers import router as drivers_router
from app.api.routes.booking_accept import router as booking_accept_router


app = FastAPI(title="UrbanGo API")
app.include_router(vehicles_router)
app.include_router(bookings_router)
app.include_router(drivers_router)
app.include_router(booking_accept_router)

