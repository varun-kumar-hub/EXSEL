import pytest
import sys
import os

# Put root directory in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.repositories import (
    user_repository,
    gate_repository,
    sensor_repository,
    alert_repository,
    event_repository,
    distribution_repository,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"
