from fastapi import APIRouter, Depends
from app.services.distribution_service import distribution_service
from app.schemas.common import APIResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/distribution", tags=["Distribution"])


@router.get("/status", response_model=APIResponse[dict])
async def get_distribution_status():
    seq = await distribution_service.get_status()
    return APIResponse(
        success=True,
        data={
            "id": seq.id,
            "name": seq.name,
            "status": seq.status,
            "current_step_index": seq.current_step_index,
            "started_at": seq.started_at,
            "completed_at": seq.completed_at,
            "steps": [
                {
                    "id": s.id,
                    "step_order": s.step_order,
                    "step_name": s.step_name,
                    "gate_target": s.gate_target,
                    "target_flow": s.target_flow,
                    "status": s.status,
                    "notes": s.notes,
                }
                for s in seq.steps
            ],
        },
    )


@router.post("/start", response_model=APIResponse[dict])
async def start_distribution(current_user: dict = Depends(get_current_user)):
    seq = await distribution_service.start_sequence(
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=True, message="Distribution sequence initiated.", data={"status": seq.status})


@router.post("/stop", response_model=APIResponse[dict])
async def stop_distribution(current_user: dict = Depends(get_current_user)):
    seq = await distribution_service.stop_sequence(
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=True, message="Distribution sequence stopped.", data={"status": seq.status})
