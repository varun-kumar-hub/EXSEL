from typing import List, Optional
from datetime import datetime
from app.database.repositories import gate_repository, event_repository
from app.database.models import GateModel
from app.hardware import get_hardware
from app.auth.permissions import permissions
from app.core.exceptions import (
    GateNotFoundError,
    GateOperationError,
    UnauthorizedOperationError,
)
from app.core.logging_config import logger


class GateService:
    def __init__(self):
        self.hardware = get_hardware()

    async def get_all_gates(self) -> List[GateModel]:
        gates = await gate_repository.get_all_gates()
        for g in gates:
            hw_status = await self.hardware.get_gate_status(g.id)
            if hw_status != g.status:
                await gate_repository.update_status(g.id, hw_status)
                g.status = hw_status
        return gates

    async def get_gate(self, gate_id: str) -> GateModel:
        gate = await gate_repository.get_by_id(gate_id)
        if not gate:
            raise GateNotFoundError(gate_id)
        hw_status = await self.hardware.get_gate_status(gate.id)
        if hw_status != gate.status:
            await gate_repository.update_status(gate.id, hw_status)
            gate.status = hw_status
        return gate

    async def execute_operation(
        self, gate_id: str, operation: str, user_role: str, operator_name: str = "Operator"
    ) -> GateModel:
        """
        Execute safety-validated gate actuation:
        1. Validate RBAC permission (Admin / Operator)
        2. Verify gate existence and connection
        3. Dispatch hardware command
        4. Update repository state
        5. Log immutable audit history event
        """
        operation = operation.upper()
        if operation not in ("OPEN", "CLOSE"):
            raise GateOperationError(f"Invalid operation '{operation}'. Must be OPEN or CLOSE.", gate_id)

        # 1. RBAC Permission Check
        if not permissions.can_control_gate(user_role):
            logger.warning(f"Unauthorized gate operation attempt on {gate_id} by role {user_role}")
            await event_repository.record_event(
                event_type="Gate Operation",
                device=gate_id,
                action=operation,
                status="Failed",
                operator=operator_name,
                metadata={"reason": "Permission denied - Viewer role"},
            )
            raise UnauthorizedOperationError("You do not have permission to control water gates.")

        # 2. Gate Status Check
        gate = await self.get_gate(gate_id)
        if not gate.is_connected:
            raise GateOperationError(f"Gate '{gate.name}' is currently offline. Actuation aborted.", gate_id)

        # 3. Hardware Dispatch
        if operation == "OPEN":
            success = await self.hardware.open_gate(gate_id)
            new_status = "OPEN"
        else:
            success = await self.hardware.close_gate(gate_id)
            new_status = "CLOSED"

        if not success:
            raise GateOperationError(f"Actuator did not respond to {operation} command on {gate.name}.", gate_id)

        # 4. Database Persistence
        updated = await gate_repository.update_status(gate_id, new_status)

        # 5. Audit Trail
        await event_repository.record_event(
            event_type="Gate Operation",
            device=gate.name,
            action=operation,
            status="Success",
            operator=operator_name,
            metadata={"gate_id": gate_id, "previous_status": gate.status},
        )
        logger.info(f"[GATE_SERVICE] Gate {gate_id} {operation} executed successfully by {operator_name}")
        return updated or gate

    async def set_mode(self, gate_id: str, mode: str, user_role: str, operator_name: str = "Operator") -> GateModel:
        mode = mode.upper()
        if mode not in ("AUTO", "MANUAL"):
            raise GateOperationError("Mode must be AUTO or MANUAL.", gate_id)

        if not permissions.can_control_gate(user_role):
            raise UnauthorizedOperationError("You do not have permission to change gate mode.")

        gate = await self.get_gate(gate_id)
        updated = await gate_repository.update_mode(gate_id, mode)

        await event_repository.record_event(
            event_type="Gate Operation",
            device=gate.name,
            action=f"MODE_{mode}",
            status="Success",
            operator=operator_name,
            metadata={"gate_id": gate_id, "mode": mode},
        )
        return updated or gate


gate_service = GateService()
