from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Smart Water Distribution System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None

    # Hardware Layer Configuration
    HARDWARE_MODE: str = "simulation"  # 'simulation' | 'esp' | 'mqtt' | 'serial'
    MQTT_BROKER: Optional[str] = None
    MQTT_PORT: int = 1883
    ESP_DEVICE_URL: Optional[str] = None

    # Security
    SECRET_KEY: str = "smart-water-system-secret-key-32-chars-long-demo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_supabase_configured(self) -> bool:
        return bool(
            self.SUPABASE_URL
            and self.SUPABASE_ANON_KEY
            and not self.SUPABASE_URL.startswith("http://placeholder")
            and len(self.SUPABASE_URL.strip()) > 10
        )


settings = Settings()
