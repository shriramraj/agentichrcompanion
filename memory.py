from __future__ import annotations
from typing import Any, Dict

class SessionMemory:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, session_id: str) -> Dict[str, Any]:
        return self._store.get(session_id, {})

    def set(self, session_id: str, data: Dict[str, Any]) -> None:
        self._store[session_id] = data
