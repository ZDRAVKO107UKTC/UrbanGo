from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import JSONB
from app.models.vehicle import Base

class BookingEventOutbox(Base):
    __tablename__ = "booking_events_outbox"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    booking_id: Mapped[int] = mapped_column(BigInteger)
    event_type: Mapped[str] = mapped_column(String(32))
    payload: Mapped[dict] = mapped_column(JSONB)
