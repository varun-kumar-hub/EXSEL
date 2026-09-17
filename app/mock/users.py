from app.core.security import hash_password
from app.config.constants import ROLE_ADMIN, ROLE_OPERATOR, ROLE_VIEWER

DEMO_USERS = [
    {
        "id": "usr-admin-01",
        "email": "admin@smartwater.io",
        "password_hash": hash_password("Admin@123"),
        "full_name": "Chief Water Admin",
        "role": ROLE_ADMIN,
        "avatar_url": None,
        "is_active": True,
    },
    {
        "id": "usr-operator-01",
        "email": "operator@smartwater.io",
        "password_hash": hash_password("Operator@123"),
        "full_name": "Sector Operator Alex",
        "role": ROLE_OPERATOR,
        "avatar_url": None,
        "is_active": True,
    },
    {
        "id": "usr-viewer-01",
        "email": "viewer@smartwater.io",
        "password_hash": hash_password("Viewer@123"),
        "full_name": "Auditor Jordan",
        "role": ROLE_VIEWER,
        "avatar_url": None,
        "is_active": True,
    },
]
