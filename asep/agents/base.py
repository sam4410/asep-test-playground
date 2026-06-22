from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from asep.domain import AgentResult


@dataclass(slots=True)
class AgentContext:
    run_id: UUID | None
    goal: str
    workspace_path: str
    memory: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    name: str
    role: str

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError
