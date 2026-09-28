from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.availability import AvailabilityEngine
from app.domain.proposal import AppointmentProposal
from app.services.approval import ApprovalService
from app.services.booking import BookingConflict, BookingService
from app.services.proposal_store import ProposalStore


def test_availability_skips_weekends() -> None:
    clinician = uuid4()
    friday = datetime(2026, 10, 2, 9, tzinfo=UTC)
    slots = AvailabilityEngine().generate(clinician, friday, days=3)
    assert all(slot.starts_at.weekday() < 5 for slot in slots)


def make_proposal() -> AppointmentProposal:
    start = datetime.now(UTC) + timedelta(hours=1)
    return AppointmentProposal.create(
        request_id=uuid4(),
        clinician_id=uuid4(),
        appointment_type="routine",
        starts_at=start,
        ends_at=start + timedelta(minutes=30),
        version=1,
        expires_at=start + timedelta(minutes=10),
        rationale="test",
    )


def test_booking_is_idempotent() -> None:
    service = BookingService()
    proposal = make_proposal()
    patient = uuid4()
    actor = uuid4()

    first = service.approve_and_book(
        idempotency_key="approve-123456",
        patient_id=patient,
        proposal=proposal,
        actor_id=actor,
    )
    second = service.approve_and_book(
        idempotency_key="approve-123456",
        patient_id=patient,
        proposal=proposal,
        actor_id=actor,
    )
    assert first == second
    assert len(service.store.appointments) == 1


def test_booking_detects_slot_conflict() -> None:
    service = BookingService()
    proposal = make_proposal()

    service.approve_and_book(
        idempotency_key="approve-first",
        patient_id=uuid4(),
        proposal=proposal,
        actor_id=uuid4(),
    )

    with pytest.raises(BookingConflict):
        service.approve_and_book(
            idempotency_key="approve-second",
            patient_id=uuid4(),
            proposal=proposal,
            actor_id=uuid4(),
        )


def test_approval_uses_server_owned_proposal() -> None:
    store = ProposalStore()
    booking = BookingService()
    service = ApprovalService(proposals=store, booking=booking)
    proposal = make_proposal()
    patient_id = uuid4()
    store.save(proposal, patient_id)

    result = service.approve(
        proposal_id=proposal.proposal_id,
        proposal_version=1,
        actor_id=uuid4(),
        idempotency_key="approve-server-owned",
    )
    assert result["proposal_id"] == str(proposal.proposal_id)


def test_stale_proposal_version_is_rejected() -> None:
    store = ProposalStore()
    service = ApprovalService(proposals=store, booking=BookingService())
    proposal = make_proposal()
    store.save(proposal, uuid4())

    with pytest.raises(ValueError, match="STALE_PROPOSAL"):
        service.approve(
            proposal_id=proposal.proposal_id,
            proposal_version=2,
            actor_id=uuid4(),
            idempotency_key="approve-stale",
        )
