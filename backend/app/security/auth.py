from dataclasses import dataclass
from uuid import UUID

from app.security.rbac import Role


@dataclass(frozen=True)
class Principal:
    subject_id: UUID
    role: Role
    clinic_id: str


def require_role(principal: Principal, *allowed_roles: Role) -> None:
    if principal.role not in allowed_roles:
        raise PermissionError("FORBIDDEN")


def require_permission(
    principal: Principal,
    permission: str,
) -> None:
    from app.security.rbac import Permission, has_permission

    try:
        requested = Permission(permission)
    except ValueError as exc:
        raise PermissionError("UNKNOWN_PERMISSION") from exc
    if not has_permission(principal.role, requested):
        raise PermissionError("FORBIDDEN")
