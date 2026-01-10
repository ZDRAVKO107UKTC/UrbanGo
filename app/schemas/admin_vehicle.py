from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    vehicle_type: str
    plate_number: Optional[str] = None
    model: str
