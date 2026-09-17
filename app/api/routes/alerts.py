from fastapi import APIRouter, Depends
from app.services.alert_service import alert_service
from app.schemas.alert import AlertCreate
from app.schemas.common import APIResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=APIResponse[list])
async def list_alerts():
    alerts = await alert_service.get_alerts()
    return APIResponse(
        success=True,
        data=[
            {
                "id": a.id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "message": a.message,
                "is_read": a.is_read,
                "created_at": a.created_at,
            }
            for a in alerts
        ],
    )


@router.post("/{alert_id}/dismiss", response_model=APIResponse[dict])
async def dismiss_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    success = await alert_service.dismiss_alert(
        alert_id=alert_id,
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=success, message="Alert dismissed.")


@router.post("", response_model=APIResponse[dict])
async def create_alert(req: AlertCreate):
    alert = await alert_service.create_alert(
        alert_type=req.alert_type,
        severity=req.severity,
        title=req.title,
        message=req.message,
    )
    return APIResponse(success=True, data={"id": alert.id, "title": alert.title})
