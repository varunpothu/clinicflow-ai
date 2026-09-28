"""add durable request, proposal, idempotency, audit and exception tables

Revision ID: 0002_operations
Revises: 0001_initial
Create Date: 2026-09-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_operations"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
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
    op.create_index("ix_appointment_requests_status", "appointment_requests", ["status"])

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
        "idempotency_keys",
        sa.Column("key", sa.String(200), primary_key=True),
        sa.Column("fingerprint", sa.String(500), nullable=False),
        sa.Column("result_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

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


def downgrade() -> None:
    op.drop_table("operational_exceptions")
    op.drop_table("audit_events")
    op.drop_table("idempotency_keys")
    op.drop_table("proposals")
    op.drop_table("appointment_requests")
