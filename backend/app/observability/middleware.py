from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.logging import logger
from app.observability.metrics import metrics
from app.observability.tracing import request_span


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
        started = perf_counter()
        with request_span(request.method, request.url.path, correlation_id):
            response = await call_next(request)
        metrics.increment("http.requests.total")
        metrics.increment(f"http.status.{response.status_code}")
        metrics.observe_latency("http.request", started)
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            correlation_id=correlation_id,
            status_code=response.status_code,
        )
        return response
