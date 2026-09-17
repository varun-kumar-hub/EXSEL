import pytest
from app.services.alert_service import alert_service


@pytest.mark.asyncio
async def test_alerts_lifecycle():
    # Fetch alerts
    alerts = await alert_service.get_alerts()
    assert len(alerts) > 0

    # Create new alert
    new_alert = await alert_service.create_alert(
        alert_type="test_alert",
        severity="warning",
        title="Test High Pressure",
        message="Simulated pressure spike detected.",
    )
    assert new_alert.id is not None

    # Dismiss alert
    dismissed = await alert_service.dismiss_alert(new_alert.id, user_role="operator")
    assert dismissed
