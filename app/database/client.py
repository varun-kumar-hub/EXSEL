from typing import Optional
from supabase import create_client, Client
from app.config.settings import settings
from app.core.logging_config import logger


class SupabaseClientManager:
    _client: Optional[Client] = None
    _initialized: bool = False

    @classmethod
    def get_client(cls) -> Optional[Client]:
        if not cls._initialized:
            cls._initialize()
        return cls._client

    @classmethod
    def _initialize(cls):
        cls._initialized = True
        if settings.is_supabase_configured:
            try:
                cls._client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_ANON_KEY
                )
                logger.info("Supabase client successfully connected.")
            except Exception as e:
                logger.warning(f"Failed to connect to Supabase: {e}. Falling back to in-memory store.")
                cls._client = None
        else:
            logger.info("Supabase credentials not configured. Running in high-fidelity in-memory mode.")
            cls._client = None


def get_db_client() -> Optional[Client]:
    return SupabaseClientManager.get_client()
