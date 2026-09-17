import uuid
from typing import Any, Dict


def generate_uuid() -> str:
    return str(uuid.uuid4())


def sanitize_dict(data: Dict[str, Any], sensitive_keys: tuple = ("password", "token", "secret")) -> Dict[str, Any]:
    """Sanitize dictionary to prevent logging sensitive information"""
    sanitized = {}
    for k, v in data.items():
        if any(s in k.lower() for s in sensitive_keys):
            sanitized[k] = "******"
        elif isinstance(v, dict):
            sanitized[k] = sanitize_dict(v, sensitive_keys)
        else:
            sanitized[k] = v
    return sanitized
