from __future__ import annotations

from collections.abc import Callable

EventHandler = Callable[[str, dict], None]


class InProcessEventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict | None = None) -> None:
        for handler in self._subscribers.get(event_type, []):
            handler(event_type, payload or {})
