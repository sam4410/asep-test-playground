from __future__ import annotations

from uuid import uuid4
from asep.db.session import session_scope
from asep.domain import Task, TaskStatus, MemoryRecord, MemoryType
from asep.repositories import RunRepository, TaskRepository, MemoryRepository, EventRepository

def test_run_repository():
    with session_scope() as session:
        run_repo = RunRepository(session)
        run = run_repo.create(goal="Create a test run")
        
        assert run.id is not None
        assert run.goal == "Create a test run"
        assert run.status == "PENDING"
        
        latest = run_repo.latest()
        assert latest is not None
        assert latest.id == run.id
        
        run_repo.update_status(run.id, "RUNNING")
        assert run.status == "RUNNING"

def test_task_repository():
    with session_scope() as session:
        run_repo = RunRepository(session)
        run = run_repo.create(goal="Goal")
        
        task_repo = TaskRepository(session)
        t = Task(title="Test Task", description="Desc", owner="coding_agent")
        row = task_repo.add_task(run.id, t)
        
        assert row.id == str(t.id)
        assert row.run_id == run.id
        assert row.status == "PENDING"
        
        tasks = task_repo.list_for_run(run.id)
        assert len(tasks) == 1
        assert tasks[0].id == row.id
        
        task_repo.update_status(t.id, TaskStatus.running)
        assert row.status == "RUNNING"

def test_memory_repository():
    with session_scope() as session:
        memory_repo = MemoryRepository(session)
        rec = MemoryRecord(
            type=MemoryType.semantic,
            key="convention",
            value={"lint": "black"},
            source="architect"
        )
        row = memory_repo.add(rec)
        
        assert row.id == str(rec.id)
        assert row.key == "convention"
        assert row.value_json == {"lint": "black"}
        
        records = memory_repo.list(MemoryType.semantic)
        assert len(records) == 1
        assert records[0].id == row.id

def test_event_repository():
    with session_scope() as session:
        event_repo = EventRepository(session)
        row = event_repo.publish("TASK_COMPLETED", source="coding_agent", payload={"task": "123"})
        
        assert row.type == "TASK_COMPLETED"
        assert row.source == "coding_agent"
        assert row.payload == {"task": "123"}
        
        events = event_repo.list_recent(limit=5)
        assert len(events) == 1
        assert events[0].id == row.id

