from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def test_create_appointment_request_accepts_structured_request() -> None:
    client = TestClient(create_app())
    patient_id = uuid4()
    response = client.post(
        "/api/v1/appointment-requests",
        headers={
            "X-Demo-Role": "PATIENT",
            "X-Demo-Subject": str(patient_id),
            "Idempotency-Key": "request-api-0001",
        },
        json={
            "patient_id": str(patient_id),
            "appointment_type": "routine",
            "natural_language": "Tuesday after 4pm",
        },
    )
    assert response.status_code == 202
    assert response.json()["next_state"] == "VALIDATING"


def test_patient_cannot_read_another_request() -> None:
    client = TestClient(create_app())
    owner = uuid4()
    other = uuid4()
    create = client.post(
        "/api/v1/appointment-requests",
        headers={
            "X-Demo-Role": "PATIENT",
            "X-Demo-Subject": str(owner),
            "Idempotency-Key": "request-api-0003",
        },
        json={"patient_id": str(owner), "appointment_type": "routine", "natural_language": "Tuesday"},
    )
    request_id = create.json()["request_id"]
    read = client.get(
        f"/api/v1/appointment-requests/{request_id}",
        headers={"X-Demo-Role": "PATIENT", "X-Demo-Subject": str(other)},
    )
    assert read.status_code == 403
