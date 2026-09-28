from collections import defaultdict
from threading import Lock
from time import perf_counter


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._counters: defaultdict[str, int] = defaultdict(int)
        self._latency_ms: defaultdict[str, list[float]] = defaultdict(list)

    def increment(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._counters[name] += amount

    def observe_latency(self, name: str, started: float) -> None:
        elapsed_ms = (perf_counter() - started) * 1000
        with self._lock:
            values = self._latency_ms[name]
            values.append(elapsed_ms)
            if len(values) > 500:
                del values[:-500]

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            latency = {
                name: {
                    "count": len(values),
                    "p50_ms": round(sorted(values)[len(values) // 2], 2) if values else 0,
                    "max_ms": round(max(values), 2) if values else 0,
                }
                for name, values in self._latency_ms.items()
            }
            return {
                "counters": dict(self._counters),
                "latency": latency,
            }


metrics = MetricsRegistry()
