from __future__ import annotations

import tempfile
import pytest
from pathlib import Path
from uuid import uuid4, UUID
from sqlalchemy import select

from asep.db.session import session_scope
from asep.db.models import RunModel, TaskModel, TaskDependencyModel
from asep.domain import Task, TaskStatus, AgentResultStatus
from asep.repositories import RunRepository, TaskRepository, EventRepository
from asep.runner import TaskRunner

def test_runner_workflow_success_and_approval_gate():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        runner = TaskRunner(workspace_path=str(tmp_path))

        with session_scope() as session:
            run_repo = RunRepository(session)
            task_repo = TaskRepository(session)
            event_repo = EventRepository(session)

            # Create a run requiring database coding and backend coding
            run = run_repo.create(goal="Create a database table and implement backend api")
            
            from asep.agents.planning import PlannerAgent
            planner = PlannerAgent()
            planned_tasks = planner.create_initial_tasks(run.goal)
            for t in planned_tasks:
                task_repo.add_task(run.id, t)

            session.commit()

            # Execute PM spec, Architect baseline, and Database Coding tasks.
            # Since dependencies are evaluated at the start of each runner cycle, we run 3 times.
            runner.run_pending_tasks()  # 1. Runs PM spec task
            runner.run_pending_tasks()  # 2. Runs Architect inspect task
            runner.run_pending_tasks()  # 3. Runs Database Coding task and pauses for approval

            # Invalidate session cache to read fresh state from DB
            session.expire_all()
            
            tasks = task_repo.list_for_run(run.id)
            task_map = {t.owner: t for t in tasks}
            
            assert task_map["product_manager"].status == "DONE"
            assert task_map["architect"].status == "DONE"
            assert task_map["database_coding_agent"].status == "PENDING_APPROVAL"
            assert task_map["backend_coding_agent"].status == "PENDING"
            
            # Simulate human approval of database task by marking it DONE
            task_repo.update_status(task_map["database_coding_agent"].id, TaskStatus.done)
            session.commit()
            
            # Run again. Database is DONE, so Backend Coding should execute and pause.
            runner.run_pending_tasks()  # 4. Runs Backend Coding and pauses
            
            session.expire_all()
            tasks = task_repo.list_for_run(run.id)
            task_map = {t.owner: t for t in tasks}
            assert task_map["backend_coding_agent"].status == "PENDING_APPROVAL"
            
            # Approve Backend Coding
            task_repo.update_status(task_map["backend_coding_agent"].id, TaskStatus.done)
            session.commit()
            
            # Run again. Refactoring, Documentation, and Reviewer should execute.
            runner.run_pending_tasks()  # 5. Runs Refactoring
            runner.run_pending_tasks()  # 6. Runs Documentation
            runner.run_pending_tasks()  # 7. Runs Reviewer
            runner.run_pending_tasks()  # 8. Evaluates that all tasks are done and marks run as DONE

            session.expire_all()
            tasks = task_repo.list_for_run(run.id)
            task_map = {t.owner: t for t in tasks}
            
            assert all(t.status == "DONE" for t in tasks)
            
            # Refresh run model to check status
            run_row = session.get(RunModel, run.id)
            assert run_row.status == "DONE"

def test_runner_retry_logic():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        runner = TaskRunner(workspace_path=str(tmp_path))

        # Mock the review agent to fail
        class FailingReviewAgent:
            name = "review_agent"
            def run(self, context):
                from asep.domain import AgentResult, AgentResultStatus
                return AgentResult(
                    agent_name=self.name,
                    status=AgentResultStatus.failed,
                    summary="Lint failure",
                    errors=["Reviewer found an error"]
                )

        runner.agents["review_agent"] = FailingReviewAgent()

        with session_scope() as session:
            run_repo = RunRepository(session)
            task_repo = TaskRepository(session)
            
            run = run_repo.create(goal="Dummy")
            
            t1 = Task(title="T1", description="", owner="review_agent")
            task_repo.add_task(run.id, t1)
            session.commit()

            # Execute 1: Should fail and increment retry_count to 1, status -> RETRY
            runner.run_pending_tasks()
            
            session.expire_all()
            task_row = session.get(TaskModel, str(t1.id))
            assert task_row.status == "RETRY"
            assert task_row.retry_count == 1
            
            # Execute 2: Exceeds max_task_retries (1), status -> FAILED, run -> FAILED
            runner.run_pending_tasks()
            
            session.expire_all()
            task_row = session.get(TaskModel, str(t1.id))
            assert task_row.status == "FAILED"
            
            run_row = session.get(RunModel, run.id)
            assert run_row.status == "FAILED"

def test_runner_blocked_dependency_propagation():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        runner = TaskRunner(workspace_path=str(tmp_path))

        with session_scope() as session:
            run_repo = RunRepository(session)
            task_repo = TaskRepository(session)
            
            run = run_repo.create(goal="Dummy")
            
            t1 = Task(title="T1", description="", owner="review_agent", status=TaskStatus.failed)
            t2 = Task(title="T2", description="", owner="documentation_agent", dependencies=[t1.id])
            
            task_repo.add_task(run.id, t1)
            task_repo.add_task(run.id, t2)
            session.commit()

            # Run. Since t1 is FAILED, t2 should transition to BLOCKED.
            runner.run_pending_tasks()
            
            session.expire_all()
            t2_row = session.get(TaskModel, str(t2.id))
            assert t2_row.status == "BLOCKED"
