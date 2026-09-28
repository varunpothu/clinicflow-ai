from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OperationalExceptionRecord(Base):
    __tablename__ = "operational_exceptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="OPEN", index=True)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    workflow_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    correlation_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    resolution_note: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
