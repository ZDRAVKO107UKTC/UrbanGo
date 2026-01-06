from pydantic import BaseModel

class VehicleOut(BaseModel):
    id: int
    vehicle_type: str
    plate_number: str | None = None
    model: str | None = None
    status: str
    available: bool

    class Config:
        from_attributes = True
