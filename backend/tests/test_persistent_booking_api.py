from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def test_persistent_proposal_requires_staff_permission() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/api/v1/persistent-booking/approvals",
        headers={
            "X-Demo-Role": "PATIENT",
            "X-Demo-Subject": str(uuid4()),
        },
    )
    assert response.status_code == 403
