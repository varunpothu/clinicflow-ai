from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    clinician_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    appointment_type: Mapped[str] = mapped_column(String(100), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDING")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rationale: Mapped[str] = mapped_column(Text(), nullable=False)
