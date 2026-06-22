from __future__ import annotations

from uuid import UUID
from datetime import datetime
from asep.domain import RequirementSpec, Task, TaskStatus, MemoryRecord, MemoryType, AgentResult, AgentResultStatus

def test_requirement_spec_validation():
    spec = RequirementSpec(
        goal="Build a feature",
        features=["feat1"],
        constraints=["constraint1"],
        acceptance_criteria=["criteria1"]
    )
    assert isinstance(spec.id, UUID)
    assert spec.goal == "Build a feature"
    assert spec.features == ["feat1"]
    assert spec.constraints == ["constraint1"]
    assert spec.acceptance_criteria == ["criteria1"]

def test_task_validation():
    task = Task(
        title="Confirm spec",
        description="Verify criteria",
        owner="product_manager"
    )
    assert isinstance(task.id, UUID)
    assert task.status == TaskStatus.pending
    assert task.priority == 100
    assert isinstance(task.created_at, datetime)

def test_memory_record_validation():
    record = MemoryRecord(
        type=MemoryType.episodic,
        key="test_key",
        value={"foo": "bar"},
        source="test"
    )
    assert isinstance(record.id, UUID)
    assert record.type == MemoryType.episodic
    assert record.value == {"foo": "bar"}
