from uuid import UUID, uuid4

from fastapi import Header, HTTPException, status

from app.core.config import get_settings
from app.security.auth import Principal
from app.security.rbac import Permission, Role, has_permission


def get_demo_principal(
    x_demo_role: str | None = Header(default=None, alias="X-Demo-Role"),
    x_demo_subject: str | None = Header(default=None, alias="X-Demo-Subject"),
) -> Principal:
    settings = get_settings()
    if settings.app_env != "local" and not x_demo_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="AUTH_REQUIRED")

    role_value = x_demo_role or Role.RECEPTIONIST.value
    try:
        role = Role(role_value)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID_ROLE") from exc

    subject_id = uuid4()
    if x_demo_subject:
        try:
            subject_id = UUID(x_demo_subject)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_SUBJECT",
            ) from exc

    return Principal(subject_id=subject_id, role=role, clinic_id="northstar")


def require_demo_permission(permission: Permission):
    def dependency(principal: Principal = __import__("fastapi").Depends(get_demo_principal)) -> Principal:
        if not has_permission(principal.role, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
        return principal

    return dependency
