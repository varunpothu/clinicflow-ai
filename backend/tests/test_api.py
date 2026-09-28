from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def test_create_appointment_request_accepts_structured_request() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/appointment-requests",
        json={"patient_id": str(uuid4()), "appointment_type": "routine", "natural_language": "Tuesday after 4pm"},
    )
    assert response.status_code == 202
    assert response.json()["next_state"] == "EXTRACTING"
