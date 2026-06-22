from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from asep.db.models import (
    EventModel,
    MemoryRecordModel,
    RunModel,
    TaskDependencyModel,
    TaskModel,
)
from asep.domain import MemoryRecord, MemoryType, Task, TaskStatus


class RunRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, goal: str, status: str = "PENDING") -> RunModel:
        run = RunModel(goal=goal, status=status)
        self.session.add(run)
        self.session.flush()
        return run

    def latest(self) -> RunModel | None:
        statement = select(RunModel).order_by(RunModel.created_at.desc()).limit(1)
        return self.session.execute(statement).scalar_one_or_none()

    def update_status(self, run_id: str | UUID, status: str) -> None:
        run = self.session.get(RunModel, str(run_id))
        if run is None:
            raise ValueError(f"Run not found: {run_id}")
        run.status = status


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_task(self, run_id: str | UUID, task: Task) -> TaskModel:
        row = TaskModel(
            id=str(task.id),
            run_id=str(run_id),
            title=task.title,
            description=task.description,
            owner=task.owner,
            priority=task.priority,
            status=task.status.value,
        )
        self.session.add(row)
        self.session.flush()

        for dependency_id in task.dependencies:
            self.session.add(
                TaskDependencyModel(
                    task_id=row.id,
                    depends_on_task_id=str(dependency_id),
                )
            )
        return row

    def list_for_run(self, run_id: str | UUID) -> list[TaskModel]:
        statement = (
            select(TaskModel)
            .where(TaskModel.run_id == str(run_id))
            .order_by(TaskModel.priority.asc(), TaskModel.created_at.asc())
        )
        return list(self.session.execute(statement).scalars())

    def list_all(self) -> list[TaskModel]:
        statement = select(TaskModel).order_by(TaskModel.created_at.desc())
        return list(self.session.execute(statement).scalars())

    def update_status(self, task_id: str | UUID, status: TaskStatus) -> None:
        task = self.session.get(TaskModel, str(task_id))
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        task.status = status.value


class MemoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, record: MemoryRecord) -> MemoryRecordModel:
        row = MemoryRecordModel(
            id=str(record.id),
            run_id=str(record.run_id) if record.run_id else None,
            type=record.type.value,
            key=record.key,
            value_json=record.value,
            source=record.source,
        )
        self.session.add(row)
        self.session.flush()
        return row

    def list(self, memory_type: MemoryType | None = None) -> list[MemoryRecordModel]:
        statement = select(MemoryRecordModel).order_by(MemoryRecordModel.created_at.desc())
        if memory_type is not None:
            statement = statement.where(MemoryRecordModel.type == memory_type.value)
        return list(self.session.execute(statement).scalars())


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def publish(
        self,
        event_type: str,
        source: str,
        payload: dict | None = None,
        run_id: str | UUID | None = None,
    ) -> EventModel:
        row = EventModel(
            run_id=str(run_id) if run_id else None,
            type=event_type,
            payload=payload or {},
            source=source,
        )
        self.session.add(row)
        self.session.flush()
        return row

    def list_recent(self, limit: int = 50) -> list[EventModel]:
        statement = select(EventModel).order_by(EventModel.created_at.desc()).limit(limit)
        return list(self.session.execute(statement).scalars())
