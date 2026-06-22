from __future__ import annotations

import subprocess
from typing import Annotated

import typer

from asep.config import load_settings
from asep.db.session import session_scope
from asep.orchestration import PlanningWorkflow
from asep.repositories import EventRepository, MemoryRepository, RunRepository, TaskRepository

app = typer.Typer(help="ASEP command line interface.")
db_app = typer.Typer(help="Database commands.")
memory_app = typer.Typer(help="Shared memory commands.")
tasks_app = typer.Typer(help="Task queue commands.")

app.add_typer(db_app, name="db")
app.add_typer(memory_app, name="memory")
app.add_typer(tasks_app, name="tasks")


@app.command()
def plan(requirement: Annotated[str, typer.Argument(help="Requirement to plan.")]) -> None:
    """Create a Phase 1 requirement spec and task graph."""
    settings = load_settings()
    workflow = PlanningWorkflow(workspace_path=str(settings.project.workspace_path))
    run_id = workflow.create_plan(requirement)
    typer.echo(f"Created plan for run {run_id}")


@app.command()
def run(requirement: Annotated[str, typer.Argument(help="Requirement to execute.")]) -> None:
    """Create a plan and execute agent tasks until approval or completion."""
    settings = load_settings()
    workflow = PlanningWorkflow(workspace_path=str(settings.project.workspace_path))
    run_id = workflow.create_plan(requirement)
    typer.echo(f"Created run {run_id}")
    
    # Start executing in-process
    typer.echo("Running agent tasks...")
    from asep.runner import TaskRunner
    runner = TaskRunner(workspace_path=str(settings.project.workspace_path))
    
    import time
    from asep.db.session import session_scope
    from asep.db.models import RunModel
    
    while True:
        runner.run_pending_tasks()
        
        with session_scope() as session:
            run_row = session.get(RunModel, str(run_id))
            status = run_row.status if run_row else "FAILED"
        
        if status == "DONE":
            typer.echo(f"Run {run_id} completed successfully!")
            break
        elif status == "FAILED":
            typer.echo(f"Run {run_id} failed!")
            break
        elif status == "PENDING_APPROVAL":
            typer.echo(f"Run {run_id} is paused waiting for human approval of the proposed patch.")
            typer.echo("Review the proposed patch under .asep/artifacts/")
            typer.echo(f"Run 'asep approve' to review and apply it.")
            break
            
        time.sleep(1)


@app.command()
def approve(task_id: Annotated[str | None, typer.Argument(help="Task ID to approve.")] = None) -> None:
    """Approve and apply proposed code change patch."""
    from pathlib import Path
    from asep.db.models import TaskModel, TaskArtifactModel
    from asep.tools.workspace import apply_patch
    from sqlalchemy import select
    
    with session_scope() as session:
        if not task_id:
            # Find latest task pending approval
            stmt = select(TaskModel).where(TaskModel.status == "PENDING_APPROVAL").order_by(TaskModel.created_at.desc()).limit(1)
            task = session.execute(stmt).scalar_one_or_none()
            if not task:
                typer.echo("No tasks are currently pending approval.")
                return
        else:
            task = session.get(TaskModel, str(task_id))
            if not task:
                typer.echo(f"Task not found: {task_id}")
                return
            if task.status != "PENDING_APPROVAL":
                typer.echo(f"Task {task.id} is not pending approval (Status: {task.status}).")
                return
        
        # Fetch the artifact path for this task's patch
        art_stmt = select(TaskArtifactModel).where(TaskArtifactModel.task_id == task.id).order_by(TaskArtifactModel.created_at.desc()).limit(1)
        artifact = session.execute(art_stmt).scalar_one_or_none()
        if not artifact:
            typer.echo(f"No proposed patch artifact found for task {task.id}.")
            return
            
        # Display the patch to user
        settings = load_settings()
        workspace = Path(settings.project.workspace_path)
        patch_file = workspace / artifact.path
        
        if not patch_file.exists():
            typer.echo(f"Patch file not found on disk: {patch_file}")
            return
            
        patch_content = patch_file.read_text(encoding="utf-8")
        typer.echo("=== PROPOSED CODE CHANGES ===")
        typer.echo(patch_content)
        typer.echo("=============================")
        
        confirm = typer.confirm("Do you want to apply these changes?")
        if not confirm:
            typer.echo("Patch rejected. Run status remains unchanged.")
            return
            
        # Find target file from diff header
        target_file = ""
        for line in patch_content.splitlines():
            if line.startswith("+++ b/"):
                target_file = line[6:].strip()
                break
            elif line.startswith("+++ "):
                target_file = line[4:].strip()
                break
                
        if not target_file:
            target_file = "dummy_feature.py"
            
        # Apply patch
        success = apply_patch(workspace, target_file, patch_content)
        if success:
            task.status = "DONE"
            # Publish event
            EventRepository(session).publish("REVIEW_COMPLETED", source="human_reviewer", payload={"task_id": task.id, "action": "approved"}, run_id=task.run_id)
            typer.echo(f"Applied patch to {target_file} successfully.")
            typer.echo(f"Task {task.id} marked as DONE.")
            
            # Continue execution loop in-process until done
            from asep.runner import TaskRunner
            runner = TaskRunner(workspace_path=str(workspace))
            typer.echo("Resuming remaining tasks...")
            
            # Commit changes so runner sees them
            session.commit()
            
            # Run in-process until done or next approval
            import time
            from asep.db.models import RunModel
            run_id = task.run_id
            while True:
                runner.run_pending_tasks()
                
                with session_scope() as session2:
                    run_row = session2.get(RunModel, str(run_id))
                    status = run_row.status if run_row else "FAILED"
                
                if status == "DONE":
                    typer.echo(f"Run {run_id} completed successfully!")
                    break
                elif status == "FAILED":
                    typer.echo(f"Run {run_id} failed!")
                    break
                elif status == "PENDING_APPROVAL":
                    typer.echo(f"Run {run_id} is paused waiting for another approval.")
                    break
                time.sleep(1)
        else:
            typer.echo("Failed to apply patch.")



@app.command()
def status() -> None:
    """Show the latest run status."""
    with session_scope() as session:
        run_row = RunRepository(session).latest()
        if run_row is None:
            typer.echo("No runs found.")
            return
        typer.echo(f"Latest run: {run_row.id}")
        typer.echo(f"Status: {run_row.status}")
        typer.echo(f"Goal: {run_row.goal}")


@db_app.command("migrate")
def db_migrate() -> None:
    """Apply Alembic migrations."""
    from alembic import command
    from alembic.config import Config
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        typer.echo("Database migrations applied successfully.")
    except Exception as e:
        typer.echo(f"Migration failed: {e}", err=True)
        raise typer.Exit(1)


@memory_app.command("list")
def memory_list() -> None:
    """List shared memory records."""
    with session_scope() as session:
        records = MemoryRepository(session).list()
        if not records:
            typer.echo("No memory records found.")
            return
        for record in records:
            typer.echo(f"{record.created_at} [{record.type}] {record.key} ({record.source})")


@tasks_app.command("list")
def tasks_list() -> None:
    """List task queue rows."""
    with session_scope() as session:
        records = TaskRepository(session).list_all()
        if not records:
            typer.echo("No tasks found.")
            return
        for task in records:
            typer.echo(f"{task.status:8} {task.priority:3} {task.owner:20} {task.title}")


@app.command()
def events(limit: int = 20) -> None:
    """List recent events."""
    with session_scope() as session:
        records = EventRepository(session).list_recent(limit=limit)
        if not records:
            typer.echo("No events found.")
            return
        for event in records:
            typer.echo(f"{event.created_at} {event.type} ({event.source})")


if __name__ == "__main__":
    app()
