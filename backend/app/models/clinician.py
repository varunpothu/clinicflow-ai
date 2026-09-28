from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Clinician(Base):
    __tablename__ = "clinicians"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    specialty: Mapped[str] = mapped_column(String(120), nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)