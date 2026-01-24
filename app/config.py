from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "Questrade Gekko-style Bot"
    environment: str = os.getenv("BOT_ENV", "development")
    refresh_token: str = os.getenv("QUESTRADE_REFRESH_TOKEN", "")
    practice: bool = os.getenv("QUESTRADE_PRACTICE", "true").lower() == "true"
    request_timeout: int = int(os.getenv("QUESTRADE_TIMEOUT", "15"))
    base_url: str = os.getenv("QUESTRADE_BASE_URL", "https://api.questrade.com")


settings = Settings()
