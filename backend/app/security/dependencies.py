from collections.abc import Callable
from uuid import UUID, uuid4

from fastapi import Depends, Header, HTTPException, status

from app.core.config import get_settings
from app.security.auth import Principal
from app.security.cognito import CognitoClaimsError, CognitoClaimsMapper
from app.security.rbac import Permission, Role, has_permission


def get_principal(
    x_demo_role: str | None = Header(default=None, alias="X-Demo-Role"),
    x_demo_subject: str | None = Header(default=None, alias="X-Demo-Subject"),
    x_principal_subject: str | None = Header(default=None, alias="X-Principal-Subject"),
    x_principal_clinic: str | None = Header(default=None, alias="X-Principal-Clinic"),
    x_principal_groups: str | None = Header(default=None, alias="X-Principal-Groups"),
) -> Principal:
    settings = get_settings()

    if settings.app_env == "local":
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

    if not x_principal_subject or not x_principal_clinic or not x_principal_groups:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="AUTH_REQUIRED")

    try:
        return CognitoClaimsMapper.to_principal(
            {
                "sub": x_principal_subject,
                "custom:clinic_id": x_principal_clinic,
                "cognito:groups": x_principal_groups,
            }
        )
    except CognitoClaimsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def require_demo_permission(permission: Permission) -> Callable[..., Principal]:
    def dependency(
        principal: Principal = Depends(get_principal),
    ) -> Principal:
        if not has_permission(principal.role, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
        return principal

    return dependency
