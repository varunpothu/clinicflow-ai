from uuid import uuid4

import pytest

from app.security.cognito import CognitoClaimsError, CognitoClaimsMapper
from app.security.rbac import Role


def test_cognito_claims_map_to_principal() -> None:
    principal = CognitoClaimsMapper.to_principal(
        {
            "sub": str(uuid4()),
            "custom:clinic_id": "northstar",
            "cognito:groups": ["RECEPTIONIST"],
        }
    )
    assert principal.role == Role.RECEPTIONIST
    assert principal.clinic_id == "northstar"


def test_cognito_mapping_fails_closed_without_role() -> None:
    with pytest.raises(CognitoClaimsError, match="ROLE_REQUIRED"):
        CognitoClaimsMapper.to_principal(
            {"sub": str(uuid4()), "custom:clinic_id": "northstar", "cognito:groups": []}
        )
