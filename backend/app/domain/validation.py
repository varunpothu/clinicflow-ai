from dataclasses import dataclass

from app.domain.appointment_request import AppointmentRequest


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


def validate_request(request: AppointmentRequest) -> ValidationResult:
    errors: list[str] = []
    if request.preferred_start and request.preferred_end and request.preferred_end <= request.preferred_start:
        errors.append("preferred_end must be after preferred_start")
    if not request.preferred_start and not request.preferred_end and not request.natural_language:
        errors.append("a time preference or natural-language request is required")
    return ValidationResult(valid=not errors, errors=tuple(errors))
