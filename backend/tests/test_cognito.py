from uuid import uuid4

import pytest

from app.security.cognito import CognitoClaimsError, CognitoClaimsMapper
from app.security.rbac import Role


def test_cognito_groups_string_maps_to_role() -> None:
    principal = CognitoClaimsMapper.to_principal({
        "sub": str(uuid4()),
        "custom:clinic_id": "northstar",
        "cognito:groups": "PATIENT",
    })
    assert principal.role == Role.PATIENT
    assert principal.clinic_id == "northstar"


def test_cognito_missing_role_is_rejected() -> None:
    with pytest.raises(CognitoClaimsError, match="ROLE_REQUIRED"):
        CognitoClaimsMapper.to_principal({
            "sub": str(uuid4()),
            "custom:clinic_id": "northstar",
            "cognito:groups": "",
        })
