import pytest
from app.services.distribution_service import distribution_service
from app.core.exceptions import UnauthorizedOperationError


@pytest.mark.asyncio
async def test_get_distribution_status():
    status = await distribution_service.get_status()
    assert status.id == "seq-main-01"
    assert len(status.steps) == 5
    assert status.steps[0].step_name == "Intake Reservoir"


@pytest.mark.asyncio
async def test_viewer_cannot_start_sequence():
    with pytest.raises(UnauthorizedOperationError):
        await distribution_service.start_sequence(user_role="viewer")


@pytest.mark.asyncio
async def test_start_and_stop_sequence():
    # Operator starts sequence
    seq = await distribution_service.start_sequence(user_role="operator", operator_name="TestOp")
    assert seq.status in ("ACTIVE", "WAITING")

    # Stop sequence
    stopped = await distribution_service.stop_sequence(user_role="operator", operator_name="TestOp")
    assert stopped.status == "FAILED"
