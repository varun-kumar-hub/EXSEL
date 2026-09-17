import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from app.database.repositories import distribution_repository, event_repository, alert_repository
from app.database.models import DistributionSequenceModel
from app.hardware import get_hardware
from app.auth.permissions import permissions
from app.core.exceptions import AppException, UnauthorizedOperationError
from app.core.logging_config import logger


class DistributionService:
    def __init__(self):
        self.hardware = get_hardware()
        self._running_task: Optional[asyncio.Task] = None

    async def get_status(self) -> DistributionSequenceModel:
        return await distribution_repository.get_current_sequence()

    async def start_sequence(self, user_role: str, operator_name: str = "Operator") -> DistributionSequenceModel:
        if not permissions.can_execute_distribution(user_role):
            raise UnauthorizedOperationError("You do not have permission to execute distribution sequences.")

        seq = await distribution_repository.get_current_sequence()
        if seq.status == "ACTIVE":
            raise AppException("A distribution sequence is already actively executing.")

        # Safety Pre-Checks
        sensor_readings = await self.hardware.read_all_sensors()
        water_level = sensor_readings.get("SENS_LVL_01", 70.0)
        if water_level < 30.0:
            raise AppException(f"Pre-check failed: Reservoir water level too low ({water_level:.1f}% < 30.0%).")

        await distribution_repository.reset_sequence()
        await distribution_repository.update_sequence_status(
            status="ACTIVE",
            current_step_index=0,
            started_at=datetime.utcnow(),
        )

        await event_repository.record_event(
            event_type="Sequence",
            device="Distribution System",
            action="START",
            status="Success",
            operator=operator_name,
            metadata={"sequence": seq.name},
        )

        # Launch automated execution task
        self._running_task = asyncio.create_task(self._run_sequence_steps(operator_name))
        return await distribution_repository.get_current_sequence()

    async def stop_sequence(self, user_role: str, operator_name: str = "Operator") -> DistributionSequenceModel:
        if not permissions.can_execute_distribution(user_role):
            raise UnauthorizedOperationError("You do not have permission to stop distribution sequences.")

        if self._running_task and not self._running_task.done():
            self._running_task.cancel()
            self._running_task = None

        seq = await distribution_repository.get_current_sequence()
        current_idx = seq.current_step_index

        if 0 <= current_idx < len(seq.steps):
            await distribution_repository.update_step_status(current_idx, "FAILED")

        await distribution_repository.update_sequence_status(
            status="FAILED",
            current_step_index=current_idx,
            completed_at=datetime.utcnow(),
        )

        await event_repository.record_event(
            event_type="Sequence",
            device="Distribution System",
            action="EMERGENCY_STOP",
            status="Warning",
            operator=operator_name,
            metadata={"interrupted_step": current_idx},
        )

        await alert_repository.create_alert(
            alert_type="sequence_aborted",
            severity="warning",
            title="Distribution Sequence Interrupted",
            message=f"Operator {operator_name} manually triggered sequence stop.",
        )
        return await distribution_repository.get_current_sequence()

    async def _run_sequence_steps(self, operator_name: str):
        """Asynchronously executes sequence steps with realistic time pacing"""
        seq = await distribution_repository.get_current_sequence()
        try:
            for idx, step in enumerate(seq.steps):
                # Mark active
                await distribution_repository.update_sequence_status(
                    status="ACTIVE", current_step_index=idx
                )
                await distribution_repository.update_step_status(idx, "ACTIVE")
                logger.info(f"[SEQUENCE] Starting step {idx+1}: {step.step_name}")

                # Actuate hardware if gate target is set
                if step.gate_target:
                    await self.hardware.open_gate(step.gate_target)

                # Pump actuation on pump step
                if "Pump" in step.step_name:
                    await self.hardware.set_pump(True)

                # Step execution duration (simulated 3 seconds per step for snappy UI feedback)
                await asyncio.sleep(3.0)

                # Mark completed
                await distribution_repository.update_step_status(idx, "COMPLETED")
                logger.info(f"[SEQUENCE] Completed step {idx+1}: {step.step_name}")

            # All steps completed
            await distribution_repository.update_sequence_status(
                status="COMPLETED",
                current_step_index=len(seq.steps),
                completed_at=datetime.utcnow(),
            )
            await event_repository.record_event(
                event_type="Sequence",
                device="Distribution System",
                action="COMPLETE",
                status="Success",
                operator="System Engine",
                metadata={"sequence": seq.name},
            )
            await alert_repository.create_alert(
                alert_type="distribution_complete",
                severity="info",
                title="Distribution Sequence Finished",
                message=f"Sequential water distribution completed across all 5 stages successfully.",
            )
        except asyncio.CancelledError:
            logger.info("[SEQUENCE] Execution task was cancelled.")
        except Exception as e:
            logger.error(f"[SEQUENCE] Error in sequence execution: {e}")
            await distribution_repository.update_sequence_status(
                status="FAILED", current_step_index=seq.current_step_index, completed_at=datetime.utcnow()
            )


distribution_service = DistributionService()
