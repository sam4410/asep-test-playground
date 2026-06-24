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

        # Initialize Git branch if enabled and not already created
        if self.settings.git.enabled:
            from asep.tools.git import GitManager
            git_mgr = GitManager(self.workspace_path)
            if git_mgr.is_git_repository():
                if not run.git_branch:
                    run_short_id = run.id[:8] if len(run.id) > 8 else run.id
                    branch_name = f"asep/run-{run_short_id}"
                    try:
                        base_branch = self.settings.git.base_branch or "main"
                        try:
                            git_mgr.checkout_branch(base_branch)
                        except Exception:
                            pass
                        git_mgr.create_and_checkout_branch(branch_name)
                        run.git_branch = branch_name
                        session.commit()
                        logger.info(f"Created and checked out git branch {branch_name} for run {run.id}")
                        event_repo.publish(
                            "GIT_BRANCH_CREATED",
                            source="runner",
                            payload={"branch_name": branch_name},
                            run_id=run.id
                        )
                        session.commit()
                    except Exception as ge:
                        logger.error(f"Failed to initialize git branch for run {run.id}: {ge}", exc_info=True)
            else:
                logger.warning(f"Git integration is enabled but workspace at {self.workspace_path} is not a git repository.")

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
                session.commit()

                # Push branch and raise PR if git is enabled
                if self.settings.git.enabled and run.git_branch and not run.github_pr_url:
                    try:
                        from asep.tools.git import GitManager, GitHubClient
                        git_mgr = GitManager(self.workspace_path)
                        git_mgr.checkout_branch(run.git_branch)

                        logger.info(f"Pushing branch {run.git_branch} to origin...")
                        git_mgr.push_branch(run.git_branch, remote="origin")

                        token = self.settings.git.github_token
                        repo = self.settings.git.github_repo
                        base = self.settings.git.base_branch or "main"

                        if token and repo:
                            logger.info(f"Creating GitHub Pull Request for repo {repo} (head: {run.git_branch}, base: {base})...")
                            pr_title = f"ASEP: {run.goal}"
                            pr_body = (
                                f"### Autonomous Software Engineering Platform (ASEP) PR\n\n"
                                f"**Goal**: {run.goal}\n\n"
                                f"#### Completed Tasks:\n"
                                + "\n".join([f"- [x] **{t.title}** ({t.owner})" for t in tasks])
                            )

                            pr_url = GitHubClient.create_pull_request(
                                repo=repo,
                                head=run.git_branch,
                                base=base,
                                title=pr_title,
                                body=pr_body,
                                token=token
                            )

                            if pr_url:
                                run.github_pr_url = pr_url
                                session.commit()
                                logger.info(f"GitHub PR created successfully: {pr_url}")
                                event_repo.publish(
                                    "PULL_REQUEST_CREATED",
                                    source="runner",
                                    payload={"pr_url": pr_url},
                                    run_id=run.id
                                )
                                session.commit()
                        else:
                            logger.warning("GitHub token or repository config not found. Skipping PR creation.")
                    except Exception as pe:
                        logger.error(f"Failed to push git branch or create GitHub PR: {pe}", exc_info=True)
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
                # Run self-healing if this is a coding task with a diff patch
                patch_artifact = next((p for p in result.artifacts if p.endswith(".diff")), None)
                if patch_artifact and task.owner in ("coding_agent", "backend_coding_agent", "frontend_coding_agent", "database_coding_agent"):
                    try:
                        patch_path = Path(self.workspace_path) / patch_artifact
                        if patch_path.exists():
                            patch_content = patch_path.read_text(encoding="utf-8")
                            
                            from asep.agents.debugging import SelfHealingAgent
                            healer = SelfHealingAgent()
                            
                            event_repo.publish(
                                "SELF_HEALING_STARTED",
                                source="runner",
                                payload={"task_id": task.id, "patch": patch_artifact},
                                run_id=run.id
                            )
                            session.commit()
                            
                            max_attempts = self.settings.execution.max_self_healing_attempts
                            val_cmd = self.settings.execution.validation_command
                            
                            healed_success, final_patch, report_content = healer.heal_task(
                                context=context,
                                original_patch=patch_content,
                                test_cmd=val_cmd,
                                max_attempts=max_attempts
                            )
                            
                            # Save final patch
                            patch_path.write_text(final_patch, encoding="utf-8")
                            
                            # Save report file
                            report_filename = f"self_healing_{run.id}_{task.id}.md"
                            report_path = Path(self.workspace_path) / ".asep" / "artifacts" / report_filename
                            report_path.write_text(report_content, encoding="utf-8")
                            
                            rel_report_path = f".asep/artifacts/{report_filename}"
                            if rel_report_path not in result.artifacts:
                                result.artifacts.append(rel_report_path)
                                
                            event_name = "SELF_HEALING_SUCCESS" if healed_success else "SELF_HEALING_FAILED"
                            event_repo.publish(
                                event_name,
                                source="runner",
                                payload={"task_id": task.id, "success": healed_success},
                                run_id=run.id
                            )
                            session.commit()
                    except Exception as she:
                        logger.error(f"Error during self-healing orchestration: {she}", exc_info=True)

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
                    meta = {}
                    if path.endswith(".diff") or path.endswith(".md"):
                        try:
                            full_path = Path(self.workspace_path) / path
                            if full_path.exists():
                                meta["content"] = full_path.read_text(encoding="utf-8")
                        except Exception as e:
                            logger.error(f"Failed to read patch content for metadata: {e}")
                    session.add(TaskArtifactModel(
                        task_id=task.id,
                        path=path,
                        kind="diff" if path.endswith(".diff") else "report",
                        metadata_json=meta
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
