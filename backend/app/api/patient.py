from fastapi import APIRouter, Depends

from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me")
def get_current_patient(
    principal: Principal = Depends(
        require_demo_permission(Permission.VIEW_OWN_APPOINTMENTS)
    ),
) -> dict[str, str]:
    return {
        "subject_id": str(principal.subject_id),
        "clinic_id": principal.clinic_id,
        "role": principal.role,
    }
