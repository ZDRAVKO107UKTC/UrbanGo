from pydantic import BaseModel, Field

class BookingCreate(BaseModel):
    rider_id: int = Field(..., gt=0)
    vehicle_id: int = Field(..., gt=0)

class BookingOut(BaseModel):
    id: int
    rider_id: int
    driver_id: int | None
    vehicle_id: int
    status: str

    class Config:
        from_attributes = True
