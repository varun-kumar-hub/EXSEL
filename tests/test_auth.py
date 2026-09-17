import pytest
from app.auth.service import auth_service
from app.utils.validators import is_password_valid, check_password_strength
from app.core.exceptions import AuthenticationError, AppException


@pytest.mark.asyncio
async def test_valid_login():
    user, token = await auth_service.login("admin@smartwater.io", "Admin@123")
    assert user is not None
    assert user.email == "admin@smartwater.io"
    assert user.role == "admin"
    assert token is not None


@pytest.mark.asyncio
async def test_invalid_password():
    with pytest.raises(AuthenticationError):
        await auth_service.login("admin@smartwater.io", "WrongPassword@123")


@pytest.mark.asyncio
async def test_nonexistent_user():
    with pytest.raises(AuthenticationError):
        await auth_service.login("nobody@smartwater.io", "Admin@123")


def test_password_strength_rules():
    # Weak password - too short
    valid, _ = is_password_valid("Short1!")
    assert not valid

    # Missing uppercase
    valid, _ = is_password_valid("lowercase123!")
    assert not valid

    # Missing number
    valid, _ = is_password_valid("NoNumbersHere!")
    assert not valid

    # Missing special character
    valid, _ = is_password_valid("NoSpecial1234")
    assert not valid

    # Valid strong password
    valid, msg = is_password_valid("StrongPass#2026")
    assert valid


import uuid

@pytest.mark.asyncio
async def test_signup_success():
    unique_id = uuid.uuid4().hex[:6]
    email = f"test_operator_{unique_id}@smartwater.io"
    user = await auth_service.signup(
        email=email,
        password="SecurePass@123",
        confirm_password="SecurePass@123",
        full_name="Test Operator",
    )
    assert user.email == email
    assert user.full_name == "Test Operator"


@pytest.mark.asyncio
async def test_signup_mismatched_passwords():
    with pytest.raises(AppException):
        await auth_service.signup(
            email="mismatch@smartwater.io",
            password="SecurePass@123",
            confirm_password="DifferentPass@123",
            full_name="Mismatch User",
        )
