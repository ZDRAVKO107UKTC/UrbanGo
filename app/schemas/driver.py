from pydantic import BaseModel

class DriverAvailabilityUpdate(BaseModel):
    driver_available: bool

class DriverAvailabilityOut(BaseModel):
    id: int
    driver_available: bool

    class Config:
        from_attributes = True
