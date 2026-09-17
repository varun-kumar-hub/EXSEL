from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from app.core.exceptions import UnauthorizedOperationError
from app.config.constants import ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER


async def get_current_user(request: Request) -> dict:
    """Retrieve authenticated user from NiceGUI storage or Authorization header"""
    # 1. Check NiceGUI app.storage.user if present
    user = getattr(request.state, "user", None)
    if user:
        return user

    # 2. Check header or session cookie
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        # In a full flow, decode token or lookup session
        # Mock/Demo session fallback
        return {
            "id": "mock-admin-id",
            "email": "admin@smartwater.io",
            "full_name": "Admin Operator",
            "role": ROLE_ADMIN,
            "is_active": True,
        }

    # Default demo user for development/API exploration if unauthenticated
    return {
        "id": "demo-operator-id",
        "email": "operator@smartwater.io",
        "full_name": "Senior Operator",
        "role": ROLE_OPERATOR,
        "is_active": True,
    }


def require_role(allowed_roles: list[str]):
    """FastAPI dependency to require specific user roles"""
    async def role_checker(user: dict = Depends(get_current_user)):
        user_role = user.get("role", ROLE_VIEWER)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of roles: {', '.join(allowed_roles)}",
            )
        return user
    return role_checker


require_admin = require_role([ROLE_ADMIN])
require_operator = require_role([ROLE_ADMIN, ROLE_OPERATOR])
