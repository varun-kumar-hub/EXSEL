from typing import List
from app.database.repositories import alert_repository, event_repository
from app.database.models import AlertModel
from app.auth.permissions import permissions
from app.core.exceptions import UnauthorizedOperationError


class AlertService:
    async def get_alerts(self, limit: int = 50) -> List[AlertModel]:
        return await alert_repository.get_all_alerts(limit=limit)

    async def get_dashboard_alerts(self, limit: int = 4) -> List[AlertModel]:
        return await alert_repository.get_active_alerts(limit=limit)

    async def dismiss_alert(self, alert_id: str, user_role: str = "operator", operator_name: str = "Operator") -> bool:
        if not permissions.can_dismiss_alerts(user_role):
            raise UnauthorizedOperationError("You do not have permission to dismiss alerts.")

        success = await alert_repository.delete_alert(alert_id)
        if success:
            await event_repository.record_event(
                event_type="Alert Dismissed",
                device="System Alerts",
                action="DISMISS",
                status="Info",
                operator=operator_name,
                metadata={"alert_id": alert_id},
            )
        return success

    async def create_alert(self, alert_type: str, severity: str, title: str, message: str) -> AlertModel:
        return await alert_repository.create_alert(alert_type, severity, title, message)


alert_service = AlertService()
