from fastapi.testclient import TestClient

from app.main import create_app


def test_patient_is_denied_audit_access() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/operations/audit", headers={"X-Demo-Role": "PATIENT"})
    assert response.status_code == 403


def test_receptionist_can_view_exceptions() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/api/v1/operations/exceptions",
        headers={"X-Demo-Role": "RECEPTIONIST"},
    )
    assert response.status_code == 200
