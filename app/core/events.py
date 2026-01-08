from __future__ import annotations
from typing import Callable, Dict, List, Any

Handler = Callable[[dict], None]

class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Handler]] = {}

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict) -> None:
        for h in self._handlers.get(event_type, []):
            h(payload)
