from fastapi import FastAPI
from app.api.routes.vehicles import router as vehicles_router

app = FastAPI(title="UrbanGo API")
app.include_router(vehicles_router)
