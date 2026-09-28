from uuid import UUID

from app.security.auth import Principal
from app.security.rbac import Role


class CognitoClaimsError(ValueError):
    pass


class CognitoClaimsMapper:
    """Maps claims verified by the edge/JWT authorizer into the app principal."""

    @staticmethod
    def to_principal(claims: dict[str, object]) -> Principal:
        subject = claims.get("sub")
        clinic_id = claims.get("custom:clinic_id") or claims.get("clinic_id")
        groups = claims.get("cognito:groups", [])

        if not isinstance(subject, str) or not subject:
            raise CognitoClaimsError("SUBJECT_REQUIRED")
        if not isinstance(clinic_id, str) or not clinic_id:
            raise CognitoClaimsError("CLINIC_REQUIRED")

        role = CognitoClaimsMapper._map_role(groups)
        try:
            subject_id = UUID(subject)
        except ValueError as exc:
            raise CognitoClaimsError("INVALID_SUBJECT") from exc

        return Principal(subject_id=subject_id, role=role, clinic_id=clinic_id)

    @staticmethod
    def _map_role(groups: object) -> Role:
        values = groups if isinstance(groups, list) else []
        for candidate in values:
            try:
                role = Role(str(candidate))
                if role != Role.SYSTEM:
                    return role
            except ValueError:
                continue
        raise CognitoClaimsError("ROLE_REQUIRED")
