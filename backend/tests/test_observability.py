from fastapi.testclient import TestClient

from app.main import create_app


def test_correlation_id_is_generated_and_returned() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/health/live")
    correlation_id = response.headers.get("X-Correlation-ID")
    assert response.status_code == 200
    assert correlation_id


def test_existing_correlation_id_is_preserved() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/api/v1/health/live",
        headers={"X-Correlation-ID": "corr-test-123"},
    )
    assert response.headers["X-Correlation-ID"] == "corr-test-123"
