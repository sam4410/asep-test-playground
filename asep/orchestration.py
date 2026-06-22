from __future__ import annotations

from asep.agents.planning import PlannerAgent, ProductManagerAgent
from asep.db.session import session_scope
from asep.domain import MemoryRecord, MemoryType
from asep.repositories import EventRepository, MemoryRepository, RunRepository, TaskRepository


class PlanningWorkflow:
    def __init__(self, workspace_path: str = ".") -> None:
        self.workspace_path = workspace_path
        self.product_manager = ProductManagerAgent()
        self.planner = PlannerAgent()

    def create_plan(self, goal: str) -> str:
        with session_scope() as session:
            runs = RunRepository(session)
            tasks = TaskRepository(session)
            memory = MemoryRepository(session)
            events = EventRepository(session)

            run = runs.create(goal=goal, status="PLANNING")
            spec = self.product_manager.create_requirement_spec(goal)
            memory.add(
                MemoryRecord(
                    run_id=run.id,
                    type=MemoryType.episodic,
                    key="requirement_spec",
                    value=spec.model_dump(mode="json"),
                    source=self.product_manager.name,
                )
            )
            events.publish(
                "REQUIREMENT_PARSED",
                source=self.product_manager.name,
                payload={"goal": goal},
                run_id=run.id,
            )

            planned_tasks = self.planner.create_initial_tasks(goal)
            for task in planned_tasks:
                tasks.add_task(run.id, task)

            memory.add(
                MemoryRecord(
                    run_id=run.id,
                    type=MemoryType.artifact,
                    key="plan_graph",
                    value={"task_ids": [str(task.id) for task in planned_tasks]},
                    source=self.planner.name,
                )
            )
            events.publish(
                "PLAN_CREATED",
                source=self.planner.name,
                payload={"task_count": len(planned_tasks)},
                run_id=run.id,
            )
            runs.update_status(run.id, "PLANNED")
            return run.id
