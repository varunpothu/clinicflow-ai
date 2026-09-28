from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class ExternalAppointment:
    external_id: str
    clinician_id: UUID
    starts_at: datetime
    ends_at: datetime
    patient_reference: str


class ClinicSchedulingSystem(Protocol):
    def is_available(self, clinician_id: UUID, starts_at: datetime) -> bool: ...

    def create_appointment(
        self,
        *,
        patient_reference: str,
        clinician_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
    ) -> ExternalAppointment: ...


class MockClinicSchedulingSystem:
    def __init__(self) -> None:
        self._appointments: dict[str, ExternalAppointment] = {}

    def is_available(self, clinician_id: UUID, starts_at: datetime) -> bool:
        return not any(
            item.clinician_id == clinician_id and item.starts_at == starts_at
            for item in self._appointments.values()
        )

    def create_appointment(
        self,
        *,
        patient_reference: str,
        clinician_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
    ) -> ExternalAppointment:
        if not self.is_available(clinician_id, starts_at):
            raise ValueError("EXTERNAL_BOOKING_CONFLICT")

        external_id = f"NS-{len(self._appointments) + 1:05d}"
        appointment = ExternalAppointment(
            external_id=external_id,
            clinician_id=clinician_id,
            starts_at=starts_at,
            ends_at=ends_at,
            patient_reference=patient_reference,
        )
        self._appointments[external_id] = appointment
        return appointment
