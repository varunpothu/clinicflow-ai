from fastapi import APIRouter

from app.observability.metrics import metrics
from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from fastapi import Depends

router = APIRouter(prefix="/metrics", tags=["operations"])


@router.get("")
def get_metrics(
    principal: Principal = Depends(
        require_demo_permission(Permission.VIEW_OPERATIONAL_EXCEPTIONS)
    ),
) -> dict[str, object]:
    del principal
    return metrics.snapshot()
