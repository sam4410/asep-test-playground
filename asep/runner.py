from __future__ import annotations

import logging
from pathlib import Path
from uuid import UUID
from sqlalchemy import select

from asep.agents.planning import ProductManagerAgent, ArchitectAgent
from asep.agents.coding import CodingAgent, BackendCodingAgent, FrontendCodingAgent, DatabaseCodingAgent
from asep.agents.refactoring import RefactoringAgent
from asep.agents.documentation import DocumentationAgent
from asep.agents.review import ReviewAgent
from asep.agents.base import AgentContext
from asep.db.session import session_scope
from asep.db.models import RunModel, TaskModel, TaskDependencyModel, AgentResultModel, TaskArtifactModel
from asep.domain import TaskStatus, AgentResultStatus, Event
from asep.repositories import EventRepository, RunRepository, TaskRepository, MemoryRepository
from asep.config import load_settings

logger = logging.getLogger("asep.runner")

class TaskRunner:
    def __init__(self, workspace_path: str = ".") -> None:
        self.workspace_path = workspace_path
        self.agents = {
            "product_manager": ProductManagerAgent(),
            "architect": ArchitectAgent(),
            "coding_agent": CodingAgent(),
            "backend_coding_agent": BackendCodingAgent(),
            "frontend_coding_agent": FrontendCodingAgent(),
            "database_coding_agent": DatabaseCodingAgent(),
            "refactoring_agent": RefactoringAgent(),
            "documentation_agent": DocumentationAgent(),
            "review_agent": ReviewAgent(),
        }
        self.settings = load_settings()

    def run_pending_tasks(self) -> None:
        """Poll and execute pending tasks across all active runs."""
        with session_scope() as session:
            # Fetch runs that are not completed or failed
            stmt = select(RunModel).where(RunModel.status.in_(["PENDING", "PLANNING", "PLANNED", "RUNNING", "PENDING_APPROVAL"]))
            active_runs = list(session.execute(stmt).scalars())

            for run in active_runs:
                try:
                    self._process_run(session, run)
                except Exception as e:
                    logger.error(f"Error processing run {run.id}: {e}", exc_info=True)

    def _process_run(self, session, run: RunModel) -> None:
        run_repo = RunRepository(session)
        task_repo = TaskRepository(session)
        event_repo = EventRepository(session)

        # Get all tasks for this run
        tasks = task_repo.list_for_run(run.id)
        if not tasks:
            return

        # Fetch dependencies
        task_ids = [t.id for t in tasks]
        dep_stmt = select(TaskDependencyModel).where(TaskDependencyModel.task_id.in_(task_ids))
        deps = list(session.execute(dep_stmt).scalars())

        # Map dependencies: task_id -> list of depends_on_task_id
        dependencies: dict[str, list[str]] = {t_id: [] for t_id in task_ids}
        for dep in deps:
            dependencies[dep.task_id].append(dep.depends_on_task_id)

        # Index tasks by ID for easy access
        task_map = {t.id: t for t in tasks}

        # Update blocked statuses based on dependencies
        for t in tasks:
            if t.status in ("PENDING", "RETRY"):
                for dep_id in dependencies[t.id]:
                    dep_task = task_map.get(dep_id)
                    if dep_task and dep_task.status in ("FAILED", "BLOCKED"):
                        task_repo.update_status(t.id, TaskStatus.blocked)
                        event_repo.publish(
                            "TASK_BLOCKED",
                            source="runner",
                            payload={"task_id": t.id, "reason": f"Dependency {dep_id} is {dep_task.status}"},
                            run_id=run.id
                        )

        # Refresh tasks list
        tasks = task_repo.list_for_run(run.id)
        task_map = {t.id: t for t in tasks}

        # Check if any task has FAILED
        if any(t.status == "FAILED" for t in tasks):
            if run.status != "FAILED":
                run_repo.update_status(run.id, "FAILED")
                event_repo.publish("RUN_FAILED", source="runner", payload={"run_id": run.id}, run_id=run.id)
            return

        # Check if all tasks are DONE
        if all(t.status == "DONE" for t in tasks):
            if run.status != "DONE":
                run_repo.update_status(run.id, "DONE")
                event_repo.publish("WORKFLOW_COMPLETED", source="runner", payload={"run_id": run.id}, run_id=run.id)
            return

        # Find ready tasks: status is PENDING or RETRY, and all dependencies are DONE
        ready_tasks = []
        has_pending_approval = False
        
        for t in tasks:
            if t.status == "PENDING_APPROVAL":
                has_pending_approval = True
            elif t.status in ("PENDING", "RETRY"):
                deps_done = True
                for dep_id in dependencies[t.id]:
                    dep_task = task_map.get(dep_id)
                    if not dep_task or dep_task.status != "DONE":
                        deps_done = False
                        break
                if deps_done:
                    ready_tasks.append(t)

        if has_pending_approval and not ready_tasks:
            # We are waiting for human approval, update run status if not set
            if run.status != "PENDING_APPROVAL":
                run_repo.update_status(run.id, "PENDING_APPROVAL")
            return

        # Dispatch ready tasks
        if ready_tasks:
            if run.status != "RUNNING":
                run_repo.update_status(run.id, "RUNNING")
            
            for task in ready_tasks:
                self._execute_task(session, run, task, task_repo, event_repo)

    def _execute_task(self, session, run: RunModel, task: TaskModel, task_repo: TaskRepository, event_repo: EventRepository) -> None:
        logger.info(f"Starting task {task.id}: {task.title} (Owner: {task.owner})")
        
        # Mark as RUNNING
        task_repo.update_status(task.id, TaskStatus.running)
        event_repo.publish("TASK_STARTED", source="runner", payload={"task_id": task.id}, run_id=run.id)
        session.commit()  # commit state change so it's visible during agent run

        agent = self.agents.get(task.owner)
        if not agent:
            # No agent implemented for this owner, fail task
            logger.error(f"No agent found for owner: {task.owner}")
            self._handle_failure(session, run, task, f"No agent implemented for owner {task.owner}", task_repo, event_repo)
            return

        # Create execution context
        context = AgentContext(
            run_id=UUID(run.id),
            goal=run.goal,
            workspace_path=self.workspace_path
        )

        try:
            result = agent.run(context)
            
            if result.status == AgentResultStatus.success:
                # Add agent result to DB
                result_row = AgentResultModel(
                    run_id=run.id,
                    task_id=task.id,
                    agent_name=agent.name,
                    status=result.status.value,
                    summary=result.summary,
                    artifacts=result.artifacts,
                    errors=[]
                )
                session.add(result_row)
                session.flush()

                # Save artifacts references
                for path in result.artifacts:
                    session.add(TaskArtifactModel(
                        task_id=task.id,
                        path=path,
                        kind="diff" if path.endswith(".diff") else "report",
                        metadata_json={}
                    ))

                # Handle Human Approval Gate for coding tasks
                if task.owner in ("coding_agent", "backend_coding_agent", "frontend_coding_agent", "database_coding_agent"):
                    task_repo.update_status(task.id, TaskStatus.pending_approval)
                    event_repo.publish(
                        "CODE_CHANGE_PROPOSED",
                        source=agent.name,
                        payload={"task_id": task.id, "artifacts": result.artifacts},
                        run_id=run.id
                    )
                else:
                    task_repo.update_status(task.id, TaskStatus.done)
                    event_repo.publish("TASK_COMPLETED", source=agent.name, payload={"task_id": task.id}, run_id=run.id)
                
                session.commit()
            else:
                error_msg = "; ".join(result.errors) or "Agent execution failed."
                self._handle_failure(session, run, task, error_msg, task_repo, event_repo)

        except Exception as e:
            logger.error(f"Execution error on task {task.id}: {e}", exc_info=True)
            self._handle_failure(session, run, task, str(e), task_repo, event_repo)

    def _handle_failure(self, session, run: RunModel, task: TaskModel, error_msg: str, task_repo: TaskRepository, event_repo: EventRepository) -> None:
        max_retries = self.settings.execution.max_task_retries
        
        # Add failure result row
        result_row = AgentResultModel(
            run_id=run.id,
            task_id=task.id,
            agent_name=task.owner,
            status=AgentResultStatus.failed.value,
            summary=f"Failure: {error_msg}",
            artifacts=[],
            errors=[error_msg]
        )
        session.add(result_row)

        if task.retry_count < max_retries:
            task.retry_count += 1
            task_repo.update_status(task.id, TaskStatus.retry)
            event_repo.publish(
                "TASK_RETRY", 
                source="runner", 
                payload={"task_id": task.id, "error": error_msg, "retry": task.retry_count},
                run_id=run.id
            )
        else:
            task_repo.update_status(task.id, TaskStatus.failed)
            # Propagate failure to run
            run_repo = RunRepository(session)
            run_repo.update_status(run.id, "FAILED")
            
            event_repo.publish(
                "TASK_FAILED", 
                source="runner", 
                payload={"task_id": task.id, "error": error_msg},
                run_id=run.id
            )
            event_repo.publish("RUN_FAILED", source="runner", payload={"run_id": run.id}, run_id=run.id)

        session.commit()
