from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    pending = "PENDING"
    running = "RUNNING"
    blocked = "BLOCKED"
    failed = "FAILED"
    retry = "RETRY"
    done = "DONE"
    pending_approval = "PENDING_APPROVAL"


class MemoryType(StrEnum):
    episodic = "episodic"
    semantic = "semantic"
    artifact = "artifact"
    long_term = "long_term"


class AgentResultStatus(StrEnum):
    success = "success"
    failed = "failed"
    blocked = "blocked"


class RequirementSpec(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    goal: str
    features: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    owner: str
    dependencies: list[UUID] = Field(default_factory=list)
    priority: int = 100
    status: TaskStatus = TaskStatus.pending
    artifacts: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PlanGraph(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    requirement_id: UUID
    tasks: list[Task]
    edges: list[tuple[UUID, UUID]] = Field(default_factory=list)
    execution_order: list[UUID] = Field(default_factory=list)


class AgentResult(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    agent_name: str
    task_id: UUID | None = None
    status: AgentResultStatus
    summary: str
    artifacts: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class MemoryRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    run_id: UUID | None = None
    type: MemoryType
    key: str
    value: dict[str, Any]
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    source: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
