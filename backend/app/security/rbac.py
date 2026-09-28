from enum import StrEnum


class Role(StrEnum):
    PATIENT = "PATIENT"
    RECEPTIONIST = "RECEPTIONIST"
    CLINICIAN = "CLINICIAN"
    ADMIN = "ADMIN"
    PLATFORM_OPERATOR = "PLATFORM_OPERATOR"
    SYSTEM = "SYSTEM"


class Permission(StrEnum):
    REQUEST_APPOINTMENT = "REQUEST_APPOINTMENT"
    VIEW_OWN_APPOINTMENTS = "VIEW_OWN_APPOINTMENTS"
    VIEW_APPROVAL_QUEUE = "VIEW_APPROVAL_QUEUE"
    APPROVE_PROPOSAL = "APPROVE_PROPOSAL"
    REJECT_PROPOSAL = "REJECT_PROPOSAL"
    MODIFY_PROPOSAL = "MODIFY_PROPOSAL"
    VIEW_CLINIC_SCHEDULE = "VIEW_CLINIC_SCHEDULE"
    MANAGE_CLINIC_CONFIG = "MANAGE_CLINIC_CONFIG"
    VIEW_OPERATIONAL_EXCEPTIONS = "VIEW_OPERATIONAL_EXCEPTIONS"
    VIEW_AUDIT = "VIEW_AUDIT"
    REPLAY_WORKFLOW = "REPLAY_WORKFLOW"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.PATIENT: frozenset(
        {Permission.REQUEST_APPOINTMENT, Permission.VIEW_OWN_APPOINTMENTS}
    ),
    Role.RECEPTIONIST: frozenset(
        {
            Permission.REQUEST_APPOINTMENT,
            Permission.VIEW_APPROVAL_QUEUE,
            Permission.APPROVE_PROPOSAL,
            Permission.REJECT_PROPOSAL,
            Permission.MODIFY_PROPOSAL,
            Permission.VIEW_CLINIC_SCHEDULE,
            Permission.VIEW_OPERATIONAL_EXCEPTIONS,
        }
    ),
    Role.CLINICIAN: frozenset({Permission.VIEW_CLINIC_SCHEDULE}),
    Role.ADMIN: frozenset(
        {
            Permission.VIEW_APPROVAL_QUEUE,
            Permission.APPROVE_PROPOSAL,
            Permission.REJECT_PROPOSAL,
            Permission.MODIFY_PROPOSAL,
            Permission.VIEW_CLINIC_SCHEDULE,
            Permission.MANAGE_CLINIC_CONFIG,
            Permission.VIEW_OPERATIONAL_EXCEPTIONS,
            Permission.VIEW_AUDIT,
        }
    ),
    Role.PLATFORM_OPERATOR: frozenset(
        {
            Permission.VIEW_OPERATIONAL_EXCEPTIONS,
            Permission.VIEW_AUDIT,
            Permission.REPLAY_WORKFLOW,
        }
    ),
    Role.SYSTEM: frozenset(),
}


def has_permission(role: Role, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS[role]
