from dataclasses import dataclass
from uuid import UUID

from app.security.rbac import Role


@dataclass(frozen=True)
class Principal:
    subject_id: UUID
    role: Role
    clinic_id: str
