from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    appointment_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    preferred_clinician_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    earliest: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latest: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
