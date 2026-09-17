from typing import Optional
from datetime import datetime
from app.database.client import get_db_client
from app.database.models import DistributionSequenceModel, DistributionStepModel
from app.mock.distribution import INITIAL_DISTRIBUTION
from app.core.logging_config import logger


class DistributionRepository:
    def __init__(self):
        steps = [
            DistributionStepModel(
                id=s["id"],
                step_order=s["step_order"],
                step_name=s["step_name"],
                status=s["status"],
                gate_target=s.get("gate_target"),
                target_flow=s.get("target_flow"),
                notes=s.get("notes"),
            )
            for s in INITIAL_DISTRIBUTION["steps"]
        ]
        self._sequence = DistributionSequenceModel(
            id=INITIAL_DISTRIBUTION["id"],
            name=INITIAL_DISTRIBUTION["name"],
            status=INITIAL_DISTRIBUTION["status"],
            current_step_index=INITIAL_DISTRIBUTION["current_step_index"],
            started_at=INITIAL_DISTRIBUTION["started_at"],
            completed_at=INITIAL_DISTRIBUTION["completed_at"],
            steps=steps,
        )

    async def get_current_sequence(self) -> DistributionSequenceModel:
        return self._sequence

    async def update_sequence_status(
        self,
        status: str,
        current_step_index: int,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ) -> DistributionSequenceModel:
        self._sequence.status = status
        self._sequence.current_step_index = current_step_index
        if started_at is not None:
            self._sequence.started_at = started_at
        if completed_at is not None:
            self._sequence.completed_at = completed_at
        return self._sequence

    async def update_step_status(self, step_index: int, status: str) -> DistributionSequenceModel:
        if 0 <= step_index < len(self._sequence.steps):
            self._sequence.steps[step_index].status = status
        return self._sequence

    async def reset_sequence(self) -> DistributionSequenceModel:
        self._sequence.status = "WAITING"
        self._sequence.current_step_index = 0
        self._sequence.started_at = None
        self._sequence.completed_at = None
        for step in self._sequence.steps:
            step.status = "WAITING"
        return self._sequence


distribution_repository = DistributionRepository()
