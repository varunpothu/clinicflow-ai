"""create initial ClinicFlow schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("external_ref", sa.String(100), nullable=False),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("contact_email", sa.String(320), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("external_ref", name="uq_patients_external_ref"),
    )
    op.create_index("ix_patients_external_ref", "patients", ["external_ref"])

    op.create_table(
        "clinicians",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("specialty", sa.String(120), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_clinicians_active", "clinicians", ["active"])

    op.create_table(
        "appointment_types",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
    )

    op.create_table(
        "appointments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("patient_id", sa.String(36), nullable=False),
        sa.Column("clinician_id", sa.String(36), nullable=False),
        sa.Column("appointment_type", sa.String(100), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="CONFIRMED"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_clinician_id", "appointments", ["clinician_id"])
    op.create_index("ix_appointments_starts_at", "appointments", ["starts_at"])
    op.create_index(
        "ux_active_clinician_start",
        "appointments",
        ["clinician_id", "starts_at"],
        unique=True,
        postgresql_where=sa.text("status IN ('HELD', 'CONFIRMED')"),
        sqlite_where=sa.text("status IN ('HELD', 'CONFIRMED')"),
    )

    op.create_table(
        "workflow_runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("request_id", sa.String(36), nullable=False),
        sa.Column("state", sa.String(40), nullable=False),
        sa.Column("correlation_id", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("failure_reason", sa.Text(), nullable=True),
    )

    op.create_table(
        "approvals",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("proposal_id", sa.String(36), nullable=False),
        sa.Column("proposal_version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="PENDING"),
        sa.Column("approver_id", sa.String(36), nullable=True),
        sa.Column("decision_reason", sa.String(1000), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "appointment_requests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("patient_id", sa.String(36), nullable=False),
        sa.Column("appointment_type", sa.String(100), nullable=False),
        sa.Column("natural_language", sa.Text(), nullable=True),
        sa.Column("status", sa.String(40), nullable=False, server_default="RECEIVED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_appointment_requests_patient_id", "appointment_requests", ["patient_id"])

    op.create_table(
        "proposals",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("request_id", sa.String(36), nullable=False),
        sa.Column("patient_id", sa.String(36), nullable=False),
        sa.Column("clinician_id", sa.String(36), nullable=False),
        sa.Column("appointment_type", sa.String(100), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(30), nullable=False, server_default="PENDING"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
    )
    op.create_index("ix_proposals_request_id", "proposals", ["request_id"])
    op.create_index("ix_proposals_patient_id", "proposals", ["patient_id"])
    op.create_index("ix_proposals_clinician_id", "proposals", ["clinician_id"])

    op.create_table(
        "workflow_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("workflow_id", sa.String(36), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("state", sa.String(40), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_workflow_events_workflow_id", "workflow_events", ["workflow_id"])

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("actor_id", sa.String(36), nullable=True),
        sa.Column("workflow_id", sa.String(36), nullable=True),
        sa.Column("entity_id", sa.String(36), nullable=True),
        sa.Column("correlation_id", sa.String(100), nullable=False),
        sa.Column("summary", sa.String(1000), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])
    op.create_index("ix_audit_events_workflow_id", "audit_events", ["workflow_id"])
    op.create_index("ix_audit_events_entity_id", "audit_events", ["entity_id"])
    op.create_index("ix_audit_events_correlation_id", "audit_events", ["correlation_id"])

    op.create_table(
        "operational_exceptions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="OPEN"),
        sa.Column("summary", sa.String(1000), nullable=False),
        sa.Column("workflow_id", sa.String(36), nullable=True),
        sa.Column("correlation_id", sa.String(100), nullable=False),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("resolution_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_operational_exceptions_code", "operational_exceptions", ["code"])
    op.create_index("ix_operational_exceptions_status", "operational_exceptions", ["status"])
    op.create_index("ix_operational_exceptions_workflow_id", "operational_exceptions", ["workflow_id"])
    op.create_index("ix_operational_exceptions_correlation_id", "operational_exceptions", ["correlation_id"])

    op.create_table(
        "idempotency_keys",
        sa.Column("key", sa.String(200), primary_key=True),
        sa.Column("fingerprint", sa.String(500), nullable=False),
        sa.Column("result_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("recipient_ref", sa.String(200), nullable=False),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="PENDING"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notifications_recipient_ref", "notifications", ["recipient_ref"])
    op.create_index("ix_notifications_status", "notifications", ["status"])

    op.create_table(
        "outbox_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("aggregate_id", sa.String(36), nullable=False),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("idempotency_keys")
    op.drop_table("operational_exceptions")
    op.drop_table("audit_events")
    op.drop_table("workflow_events")
    op.drop_table("proposals")
    op.drop_table("appointment_requests")
    op.drop_table("outbox_events")
    op.drop_table("approvals")
    op.drop_table("workflow_runs")
    op.drop_index("ux_active_clinician_start", table_name="appointments")
    op.drop_table("appointments")
    op.drop_table("appointment_types")
    op.drop_index("ix_clinicians_active", table_name="clinicians")
    op.drop_table("clinicians")
    op.drop_index("ix_patients_external_ref", table_name="patients")
    op.drop_table("patients")
