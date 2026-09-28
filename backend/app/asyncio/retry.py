from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0

    def delay_for(self, attempt: int) -> float:
        if attempt < 1:
            raise ValueError("attempt must be >= 1")
        multiplier = float(2 ** (attempt - 1))
        delay = self.base_delay_seconds * multiplier
        return float(min(delay, self.max_delay_seconds))
