from app.auth.permissions import permissions
from app.config.constants import ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER


def test_rbac_permissions():
    # Admin has all permissions
    assert permissions.can_control_gate(ROLE_ADMIN)
    assert permissions.can_execute_distribution(ROLE_ADMIN)
    assert permissions.can_manage_users(ROLE_ADMIN)
    assert permissions.can_access_settings(ROLE_ADMIN)

    # Operator can control equipment but cannot manage users
    assert permissions.can_control_gate(ROLE_OPERATOR)
    assert permissions.can_execute_distribution(ROLE_OPERATOR)
    assert not permissions.can_manage_users(ROLE_OPERATOR)

    # Viewer has read-only access (no gate control, no distribution actuation)
    assert not permissions.can_control_gate(ROLE_VIEWER)
    assert not permissions.can_execute_distribution(ROLE_VIEWER)
    assert not permissions.can_manage_users(ROLE_VIEWER)
    assert not permissions.can_access_settings(ROLE_VIEWER)
    assert permissions.can_view_dashboard(ROLE_VIEWER)
    assert permissions.can_view_sensors(ROLE_VIEWER)
