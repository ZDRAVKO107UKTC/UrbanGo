from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, BigInteger, text

class Base(DeclarativeBase):
    pass

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vehicle_type: Mapped[str] = mapped_column(String(16))
    plate_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    model: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(String(16))
    available: Mapped[bool] = mapped_column(Boolean)
