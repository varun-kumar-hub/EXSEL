from fastapi import APIRouter, HTTPException, Depends
from app.services.gate_service import gate_service
from app.schemas.gate import GateOperationRequest, GateModeRequest, GateResponse
from app.schemas.common import APIResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/gates", tags=["Water Gates"])


@router.get("", response_model=APIResponse[list])
async def list_gates():
    gates = await gate_service.get_all_gates()
    return APIResponse(
        success=True,
        data=[
            {
                "id": g.id,
                "name": g.name,
                "location": g.location,
                "status": g.status,
                "mode": g.mode,
                "is_connected": g.is_connected,
                "last_changed_at": g.last_changed_at,
            }
            for g in gates
        ],
    )


@router.get("/{gate_id}", response_model=APIResponse[dict])
async def get_gate(gate_id: str):
    gate = await gate_service.get_gate(gate_id)
    return APIResponse(
        success=True,
        data={
            "id": gate.id,
            "name": gate.name,
            "location": gate.location,
            "status": gate.status,
            "mode": gate.mode,
            "is_connected": gate.is_connected,
            "last_changed_at": gate.last_changed_at,
        },
    )


@router.post("/{gate_id}/open", response_model=APIResponse[dict])
async def open_gate(gate_id: str, current_user: dict = Depends(get_current_user)):
    gate = await gate_service.execute_operation(
        gate_id=gate_id,
        operation="OPEN",
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=True, message=f"Gate {gate_id} opened successfully.", data={"status": gate.status})


@router.post("/{gate_id}/close", response_model=APIResponse[dict])
async def close_gate(gate_id: str, current_user: dict = Depends(get_current_user)):
    gate = await gate_service.execute_operation(
        gate_id=gate_id,
        operation="CLOSE",
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=True, message=f"Gate {gate_id} closed successfully.", data={"status": gate.status})


@router.post("/{gate_id}/mode", response_model=APIResponse[dict])
async def set_gate_mode(gate_id: str, req: GateModeRequest, current_user: dict = Depends(get_current_user)):
    gate = await gate_service.set_mode(
        gate_id=gate_id,
        mode=req.mode,
        user_role=current_user.get("role", "viewer"),
        operator_name=current_user.get("full_name", "Operator"),
    )
    return APIResponse(success=True, message=f"Gate mode set to {req.mode}.", data={"mode": gate.mode})
