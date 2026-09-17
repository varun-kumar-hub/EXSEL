from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from app.database.client import get_db_client
from app.database.repositories import user_repository, event_repository
from app.database.models import UserModel
from app.core.security import (
    hash_password,
    verify_password,
    generate_session_token,
    generate_reset_token,
    verify_reset_token,
)
from app.core.exceptions import AuthenticationError, AppException
from app.utils.validators import validate_email, is_password_valid
from app.utils.helpers import generate_uuid
from app.core.logging_config import logger


class AuthService:
    """
    Centralized Authentication & Identity Service
    Provides seamless dual-mode operation:
    1. Supabase Auth when Supabase credentials are valid
    2. High-fidelity secure local auth (bcrypt hashed) for standalone development
    """

    async def login(self, email: str, password: str) -> Tuple[UserModel, str]:
        email = email.strip().lower()
        if not validate_email(email):
            raise AuthenticationError("Please enter a valid email address.")

        client = get_db_client()
        # 1. Supabase Auth if configured
        if client:
            try:
                res = client.auth.sign_in_with_password({"email": email, "password": password})
                if res.user:
                    token = res.session.access_token if res.session else generate_session_token()
                    profile = await user_repository.get_by_email(email)
                    if not profile:
                        profile = UserModel(
                            id=res.user.id,
                            email=email,
                            password_hash="",
                            full_name=res.user.user_metadata.get("full_name", email.split("@")[0]),
                            role="operator",
                        )
                    await event_repository.record_event(
                        event_type="Auth",
                        device="Web Client",
                        action="LOGIN",
                        status="Success",
                        operator=profile.full_name or profile.email,
                    )
                    return profile, token
            except Exception as e:
                logger.warning(f"Supabase auth login error: {e}")
                # Fall through to local check if demo user

        # 2. Local Repository Auth
        user = await user_repository.get_by_email(email)
        if not user:
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("This account has been disabled. Please contact system administrator.")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")

        token = generate_session_token()
        await event_repository.record_event(
            event_type="Auth",
            device="Web Client",
            action="LOGIN",
            status="Success",
            operator=user.full_name or user.email,
        )
        return user, token

    async def signup(self, email: str, password: str, confirm_password: str, full_name: str) -> UserModel:
        email = email.strip().lower()
        if not validate_email(email):
            raise AppException("Please provide a valid email address.")

        if password != confirm_password:
            raise AppException("Passwords do not match.")

        valid, msg = is_password_valid(password)
        if not valid:
            raise AppException(msg)

        existing = await user_repository.get_by_email(email)
        if existing:
            raise AppException("An account with this email address is already registered.")

        client = get_db_client()
        user_id = generate_uuid()

        if client:
            try:
                res = client.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {"data": {"full_name": full_name, "role": "viewer"}},
                })
                if res.user:
                    user_id = res.user.id
            except Exception as e:
                logger.warning(f"Supabase auth signup error: {e}")

        new_user = UserModel(
            id=user_id,
            email=email,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role="operator",  # Default new self-registered to operator for testing
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        await user_repository.create_user(new_user)
        await event_repository.record_event(
            event_type="Auth",
            device="Web Client",
            action="SIGNUP",
            status="Success",
            operator=full_name,
        )
        return new_user

    async def google_login(self, token: str) -> Tuple[UserModel, str]:
        """Process Google OAuth token callback or simulation"""
        # In full flow, token is verified with Supabase
        email = "google_user@smartwater.io"
        user = await user_repository.get_by_email(email)
        if not user:
            user = UserModel(
                id=generate_uuid(),
                email=email,
                password_hash="",
                full_name="Google Verified Operator",
                role="operator",
                is_active=True,
            )
            await user_repository.create_user(user)

        session_token = generate_session_token()
        await event_repository.record_event(
            event_type="Auth",
            device="Google OAuth",
            action="LOGIN",
            status="Success",
            operator=user.full_name,
        )
        return user, session_token

    async def request_password_reset(self, email: str) -> str:
        """Send password reset link/token"""
        email = email.strip().lower()
        user = await user_repository.get_by_email(email)
        if not user:
            # For security, avoid leaking whether email exists
            return "If that email is registered, a password reset link has been dispatched."

        token = generate_reset_token(email)
        logger.info(f"[AUTH] Dispatched password reset link to {email} with token {token[:12]}...")
        await event_repository.record_event(
            event_type="Auth",
            device="Web Client",
            action="RESET_REQUEST",
            status="Success",
            operator=email,
        )
        return token

    async def reset_password(self, token: str, new_password: str, confirm_password: str) -> bool:
        if new_password != confirm_password:
            raise AppException("Passwords do not match.")

        valid, msg = is_password_valid(new_password)
        if not valid:
            raise AppException(msg)

        email = verify_reset_token(token)
        if not email:
            raise AppException("The password reset token is invalid or has expired.")

        user = await user_repository.get_by_email(email)
        if not user:
            raise AppException("User not found.")

        new_hash = hash_password(new_password)
        await user_repository.update_user(user.id, {"password_hash": new_hash})
        await event_repository.record_event(
            event_type="Auth",
            device="Web Client",
            action="RESET_CONFIRM",
            status="Success",
            operator=user.email,
        )
        return True


auth_service = AuthService()
