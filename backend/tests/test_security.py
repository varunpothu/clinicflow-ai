from uuid import uuid4

import pytest

from app.security.rbac import Permission, Role, has_permission
from app.security.auth import Principal, require_permission


def test_patient_cannot_approve() -> None:
    assert not has_permission(Role.PATIENT, Permission.APPROVE_PROPOSAL)


def test_receptionist_can_approve() -> None:
    assert has_permission(Role.RECEPTIONIST, Permission.APPROVE_PROPOSAL)


def test_unknown_permission_fails_closed() -> None:
    principal = Principal(subject_id=uuid4(), role=Role.PATIENT, clinic_id="northstar")
    with pytest.raises(PermissionError, match="UNKNOWN_PERMISSION"):
        require_permission(principal, "NOT_A_PERMISSION")
