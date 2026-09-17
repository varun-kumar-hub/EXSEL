from typing import Optional, List
from datetime import datetime
from app.database.client import get_db_client
from app.database.models import GateModel
from app.mock.gates import INITIAL_GATES
from app.core.logging_config import logger


class GateRepository:
    def __init__(self):
        self._memory_gates: dict[str, GateModel] = {}
        for g in INITIAL_GATES:
            gate = GateModel(
                id=g["id"],
                name=g["name"],
                location=g["location"],
                status=g["status"],
                mode=g["mode"],
                is_connected=g["is_connected"],
                last_changed_at=g["last_changed_at"],
            )
            self._memory_gates[gate.id] = gate

    async def get_all_gates(self) -> List[GateModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("gates").select("*").order("id").execute()
                if res.data:
                    return [
                        GateModel(
                            id=d["id"],
                            name=d["name"],
                            location=d["location"],
                            status=d["status"],
                            mode=d["mode"],
                            is_connected=d.get("is_connected", True),
                            last_changed_at=datetime.fromisoformat(d["last_changed_at"].replace("Z", "+00:00")) if d.get("last_changed_at") else datetime.utcnow(),
                        )
                        for d in res.data
                    ]
            except Exception as e:
                logger.warning(f"Supabase error fetching gates: {e}")
        return list(self._memory_gates.values())

    async def get_by_id(self, gate_id: str) -> Optional[GateModel]:
        client = get_db_client()
        if client:
            try:
                res = client.table("gates").select("*").eq("id", gate_id).execute()
                if res.data:
                    d = res.data[0]
                    return GateModel(
                        id=d["id"],
                        name=d["name"],
                        location=d["location"],
                        status=d["status"],
                        mode=d["mode"],
                        is_connected=d.get("is_connected", True),
                        last_changed_at=datetime.fromisoformat(d["last_changed_at"].replace("Z", "+00:00")) if d.get("last_changed_at") else datetime.utcnow(),
                    )
            except Exception as e:
                logger.warning(f"Supabase error fetching gate {gate_id}: {e}")
        return self._memory_gates.get(gate_id)

    async def update_status(self, gate_id: str, status: str) -> Optional[GateModel]:
        gate = self._memory_gates.get(gate_id)
        if gate:
            gate.status = status
            gate.last_changed_at = datetime.utcnow()

        client = get_db_client()
        if client:
            try:
                client.table("gates").update({
                    "status": status,
                    "last_changed_at": datetime.utcnow().isoformat(),
                }).eq("id", gate_id).execute()
            except Exception as e:
                logger.warning(f"Supabase error updating gate status: {e}")

        return gate

    async def update_mode(self, gate_id: str, mode: str) -> Optional[GateModel]:
        gate = self._memory_gates.get(gate_id)
        if gate:
            gate.mode = mode
            gate.last_changed_at = datetime.utcnow()

        client = get_db_client()
        if client:
            try:
                client.table("gates").update({
                    "mode": mode,
                    "last_changed_at": datetime.utcnow().isoformat(),
                }).eq("id", gate_id).execute()
            except Exception as e:
                logger.warning(f"Supabase error updating gate mode: {e}")

        return gate


gate_repository = GateRepository()
