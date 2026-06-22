from __future__ import annotations

from collections import defaultdict, deque
from uuid import UUID

from asep.domain import Task


def resolve_execution_order(tasks: list[Task]) -> list[UUID]:
    task_ids = {task.id for task in tasks}
    incoming_counts: dict[UUID, int] = {task.id: 0 for task in tasks}
    outgoing: dict[UUID, list[UUID]] = defaultdict(list)

    for task in tasks:
        for dependency_id in task.dependencies:
            if dependency_id not in task_ids:
                raise ValueError(f"Task {task.id} depends on unknown task {dependency_id}")
            incoming_counts[task.id] += 1
            outgoing[dependency_id].append(task.id)

    ready = deque(task_id for task_id, count in incoming_counts.items() if count == 0)
    ordered: list[UUID] = []

    while ready:
        task_id = ready.popleft()
        ordered.append(task_id)
        for child_id in outgoing[task_id]:
            incoming_counts[child_id] -= 1
            if incoming_counts[child_id] == 0:
                ready.append(child_id)

    if len(ordered) != len(tasks):
        raise ValueError("Task graph contains a cycle")

    return ordered
