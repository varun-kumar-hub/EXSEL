import pytest
from app.services.gate_service import gate_service
from app.core.exceptions import UnauthorizedOperationError, GateNotFoundError


@pytest.mark.asyncio
async def test_get_all_gates():
    gates = await gate_service.get_all_gates()
    assert len(gates) == 4
    gate_ids = [g.id for g in gates]
    assert "GATE_01" in gate_ids
    assert "GATE_04" in gate_ids


@pytest.mark.asyncio
async def test_gate_open_close_operation():
    # Operator can open Gate 04
    gate = await gate_service.execute_operation(
        gate_id="GATE_04",
        operation="OPEN",
        user_role="operator",
        operator_name="Alex",
    )
    assert gate.status in ("OPEN", "OPENING")

    # Operator can close Gate 04
    gate = await gate_service.execute_operation(
        gate_id="GATE_04",
        operation="CLOSE",
        user_role="operator",
        operator_name="Alex",
    )
    assert gate.status in ("CLOSED", "CLOSING")


@pytest.mark.asyncio
async def test_viewer_cannot_control_gate():
    with pytest.raises(UnauthorizedOperationError):
        await gate_service.execute_operation(
            gate_id="GATE_01",
            operation="CLOSE",
            user_role="viewer",
            operator_name="Jordan",
        )


@pytest.mark.asyncio
async def test_nonexistent_gate():
    with pytest.raises(GateNotFoundError):
        await gate_service.execute_operation(
            gate_id="GATE_INVALID_99",
            operation="OPEN",
            user_role="admin",
        )
