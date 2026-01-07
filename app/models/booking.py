from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from app.models.vehicle import Base

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    rider_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"))
    driver_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("vehicles.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(16))
