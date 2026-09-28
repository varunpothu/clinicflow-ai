from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def test_patient_endpoint_requires_authenticated_demo_subject() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/patients/me", headers={"X-Demo-Role": "PATIENT"})
    assert response.status_code == 401


def test_patient_endpoint_returns_principal() -> None:
    client = TestClient(create_app())
    subject = uuid4()
    response = client.get(
        "/api/v1/patients/me",
        headers={"X-Demo-Role": "PATIENT", "X-Demo-Subject": str(subject)},
    )
    assert response.status_code == 200
    assert response.json()["subject_id"] == str(subject)
