from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        Index(
            "ux_active_clinician_start",
            "clinician_id",
            "starts_at",
            unique=True,
            postgresql_where=text("status IN ('HELD', 'CONFIRMED')"),
            sqlite_where=text("status IN ('HELD', 'CONFIRMED')"),
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    patient_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    clinician_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    appointment_type: Mapped[str] = mapped_column(String(100), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="CONFIRMED")
    version: Mapped[int] = mapped_column(nullable=False, default=1)
