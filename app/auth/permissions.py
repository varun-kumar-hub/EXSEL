from app.config.constants import ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER


class PermissionManager:
    """
    Role-Based Access Control (RBAC) Engine
    Strictly enforces permission boundaries per the PRD specification:
    - Admin: Full system control, user management, and system settings
    - Operator: Gate control, distribution execution, monitoring, history, limited settings
    - Viewer: Read-only monitoring (Dashboard, Sensors, Gates, Analytics, History)
    """

    @staticmethod
    def can_control_gate(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR)

    @staticmethod
    def can_execute_distribution(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR)

    @staticmethod
    def can_view_dashboard(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER)

    @staticmethod
    def can_view_sensors(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER)

    @staticmethod
    def can_view_analytics(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER)

    @staticmethod
    def can_view_history(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER)

    @staticmethod
    def can_access_settings(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR)

    @staticmethod
    def can_manage_users(role: str) -> bool:
        return role == ROLE_ADMIN

    @staticmethod
    def can_dismiss_alerts(role: str) -> bool:
        return role in (ROLE_ADMIN, ROLE_OPERATOR)


permissions = PermissionManager()
