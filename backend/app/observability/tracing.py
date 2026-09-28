from contextlib import contextmanager
from typing import Iterator

from opentelemetry import trace


_tracer = trace.get_tracer("clinicflow-ai")


@contextmanager
def request_span(method: str, path: str, correlation_id: str) -> Iterator[object]:
    with _tracer.start_as_current_span("http.request") as span:
        span.set_attribute("http.request.method", method)
        span.set_attribute("url.path", path)
        span.set_attribute("clinicflow.correlation_id", correlation_id)
        yield span
