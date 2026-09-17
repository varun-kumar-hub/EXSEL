from fastapi import APIRouter, HTTPException, status, Depends
from app.auth.service import auth_service
from app.schemas.user import (
    UserLogin,
    UserCreate,
    PasswordResetRequest,
    PasswordResetConfirm,
    UserResponse,
)
from app.schemas.common import APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=APIResponse[dict])
async def login(req: UserLogin):
    try:
        user, token = await auth_service.login(req.email, req.password)
        return APIResponse(
            success=True,
            message="Login successful",
            data={
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                },
                "token": token,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/signup", response_model=APIResponse[dict])
async def signup(req: UserCreate):
    try:
        user = await auth_service.signup(
            email=req.email,
            password=req.password,
            confirm_password=req.confirm_password,
            full_name=req.full_name,
        )
        return APIResponse(
            success=True,
            message="Account created successfully",
            data={"id": user.id, "email": user.email, "role": user.role},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/forgot-password", response_model=APIResponse[dict])
async def forgot_password(req: PasswordResetRequest):
    msg = await auth_service.request_password_reset(req.email)
    return APIResponse(success=True, message=msg)


@router.post("/reset-password", response_model=APIResponse[dict])
async def reset_password(req: PasswordResetConfirm):
    try:
        await auth_service.reset_password(req.token, req.new_password, req.confirm_password)
        return APIResponse(success=True, message="Password updated successfully.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
