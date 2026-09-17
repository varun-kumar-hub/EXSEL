import hashlib
import hmac
import secrets
from datetime import datetime
import bcrypt
from app.config.settings import settings

def hash_password(password: str) -> str:
    """Securely hash a password with bcrypt"""
    # bcrypt enforces a 72-byte max length limit
    pw_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash"""
    try:
        pw_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return False


def generate_session_token() -> str:
    """Generate a secure random session token"""
    return secrets.token_urlsafe(32)


def generate_reset_token(email: str) -> str:
    """Generate a signed password reset token"""
    timestamp = str(int(datetime.utcnow().timestamp()))
    data = f"{email}:{timestamp}"
    signature = hmac.new(
        settings.SECRET_KEY.encode(), data.encode(), hashlib.sha256
    ).hexdigest()
    return f"{data}:{signature}"


def verify_reset_token(token: str, max_age_seconds: int = 3600) -> str:
    """Verify reset token and return email if valid, else None"""
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        email, timestamp_str, signature = parts
        timestamp = int(timestamp_str)
        now = int(datetime.utcnow().timestamp())

        if now - timestamp > max_age_seconds:
            return None

        data = f"{email}:{timestamp_str}"
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode(), data.encode(), hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(signature, expected_sig):
            return email
        return None
    except Exception:
        return None
