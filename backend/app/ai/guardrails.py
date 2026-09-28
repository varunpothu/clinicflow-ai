from re import Pattern, compile


MAX_INPUT_CHARS = 4000

_PROMPT_INJECTION_PATTERNS: tuple[Pattern[str], ...] = (
    compile(r"ignore\s+(all|any|the)\s+(previous|prior|system)\s+instructions", flags=2),
    compile(r"reveal\s+(the\s+)?system\s+prompt", flags=2),
    compile(r"show\s+(me\s+)?your\s+hidden\s+instructions", flags=2),
)


class UnsafeInputError(ValueError):
    pass


def validate_user_text(text: str) -> str:
    normalized = text.strip()
    if not normalized:
        raise UnsafeInputError("EMPTY_INPUT")
    if len(normalized) > MAX_INPUT_CHARS:
        raise UnsafeInputError("INPUT_TOO_LONG")
    if any(pattern.search(normalized) for pattern in _PROMPT_INJECTION_PATTERNS):
        raise UnsafeInputError("PROMPT_INJECTION_DETECTED")
    return normalized