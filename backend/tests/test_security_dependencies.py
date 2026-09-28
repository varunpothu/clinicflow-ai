from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.core.config import Settings
from app.security import dependencies
from app.security.rbac import Role


def test_production_principal_uses_verified_claim_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        dependencies,
        "get_settings",
        lambda: Settings(app_env="production"),
    )
    subject = uuid4()
    principal = dependencies.get_principal(
        x_principal_subject=str(subject),
        x_principal_clinic="northstar",
        x_principal_groups="PATIENT",
    )
    assert principal.subject_id == subject
    assert principal.role == Role.PATIENT
    assert principal.clinic_id == "northstar"


def test_production_principal_rejects_missing_claims(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        dependencies,
        "get_settings",
        lambda: Settings(app_env="production"),
    )
    with pytest.raises(HTTPException) as exc:
        dependencies.get_principal()
    assert exc.value.status_code == 401
