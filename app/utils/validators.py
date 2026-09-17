import re
from typing import Tuple, Dict


def validate_email(email: str) -> bool:
    """Validate email format with regex"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))


def check_password_strength(password: str) -> Dict[str, bool]:
    """
    Validate password against the 4 PRD criteria:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one number
    - At least one special character
    """
    return {
        "min_length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "number": bool(re.search(r"[0-9]", password)),
        "special_char": bool(re.search(r"[@#$%^&+=!_~*?<>{}\[\]|:;.,-]", password)),
    }


def is_password_valid(password: str) -> Tuple[bool, str]:
    """Return whether password meets all requirements with a message"""
    checks = check_password_strength(password)
    if not checks["min_length"]:
        return False, "Password must be at least 8 characters long."
    if not checks["uppercase"]:
        return False, "Password must contain at least one uppercase letter."
    if not checks["number"]:
        return False, "Password must contain at least one number."
    if not checks["special_char"]:
        return False, "Password must contain at least one special character (@, #, $, %, etc.)."
    return True, "Password meets strength criteria."
