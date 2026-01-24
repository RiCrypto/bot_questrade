from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BotState:
    running: bool = False
    mode: str = "paper"
    strategy: str = "momentum"
    last_action: str | None = None
    logs: list[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.logs.append(f"[{timestamp}] {message}")
        self.logs = self.logs[-200:]
