from app.observability.tracing import request_span


def test_request_span_can_be_created() -> None:
    with request_span("GET", "/api/v1/health/live", "corr-test"):
        pass
