from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import select

from asep.config import load_settings
from asep.db.session import session_scope
from asep.db.models import RunModel, TaskModel, TaskDependencyModel, MemoryRecordModel, EventModel, TaskArtifactModel
from asep.orchestration import PlanningWorkflow
from asep.repositories import EventRepository
from asep.tools.workspace import apply_patch

app = FastAPI(title="ASEP", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    import os
    import alembic.config
    import alembic.command
    from asep.config import load_settings
    
    def mask_url(url: str | None) -> str:
        if not url:
            return "None"
        if "@" in url:
            try:
                parts = url.split("@", 1)
                scheme_and_user = parts[0]
                if ":" in scheme_and_user:
                    subparts = scheme_and_user.split(":")
                    # Keep scheme and username, mask password
                    return f"{subparts[0]}:{subparts[1]}:***@{parts[1]}"
            except Exception:
                pass
        return "URL-present-but-failed-to-mask"

    env_url = os.environ.get("DATABASE_URL")
    settings = load_settings()
    config_url = settings.database.url

    print(f"DATABASE_URL in os.environ: {mask_url(env_url)}")
    print(f"DATABASE_URL in load_settings: {mask_url(config_url)}")
    print("Running database migrations on startup...")
    try:
        alembic_cfg = alembic.config.Config("alembic.ini")
        alembic.command.upgrade(alembic_cfg, "head")
        print("Database migrations applied successfully.")
    except Exception as e:
        print(f"Error running database migrations: {e}")



class PlanRequest(BaseModel):
    requirement: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


@app.post("/plans")
def create_plan_legacy(request: PlanRequest) -> dict[str, str]:
    run_id = PlanningWorkflow().create_plan(request.requirement)
    return {"run_id": run_id, "status": "PLANNED"}


@app.post("/api/v1/runs")
def create_run(request: PlanRequest) -> dict[str, str]:
    run_id = PlanningWorkflow().create_plan(request.requirement)
    return {"run_id": run_id, "status": "PLANNED"}


@app.get("/api/v1/runs")
def list_runs() -> list[dict]:
    with session_scope() as session:
        stmt = select(RunModel).order_by(RunModel.created_at.desc())
        runs = session.execute(stmt).scalars().all()
        return [
            {
                "id": r.id,
                "goal": r.goal,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in runs
        ]


@app.get("/api/v1/runs/{run_id}")
def get_run(run_id: str) -> dict:
    with session_scope() as session:
        run = session.get(RunModel, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return {
            "id": run.id,
            "goal": run.goal,
            "status": run.status,
            "created_at": run.created_at.isoformat() if run.created_at else None,
            "updated_at": run.updated_at.isoformat() if run.updated_at else None,
        }


@app.get("/api/v1/runs/{run_id}/tasks")
def get_run_tasks(run_id: str) -> list[dict]:
    with session_scope() as session:
        stmt = select(TaskModel).where(TaskModel.run_id == run_id).order_by(TaskModel.priority.asc(), TaskModel.created_at.asc())
        tasks = session.execute(stmt).scalars().all()
        
        task_ids = [t.id for t in tasks]
        dep_stmt = select(TaskDependencyModel).where(TaskDependencyModel.task_id.in_(task_ids))
        deps = session.execute(dep_stmt).scalars().all()
        
        dependencies = {t_id: [] for t_id in task_ids}
        for dep in deps:
            dependencies[dep.task_id].append(dep.depends_on_task_id)
            
        return [
            {
                "id": t.id,
                "run_id": t.run_id,
                "title": t.title,
                "description": t.description,
                "owner": t.owner,
                "priority": t.priority,
                "status": t.status,
                "retry_count": t.retry_count,
                "dependencies": dependencies[t.id],
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "updated_at": t.updated_at.isoformat() if t.updated_at else None,
            }
            for t in tasks
        ]


@app.get("/api/v1/runs/{run_id}/memory")
def get_run_memory(run_id: str) -> list[dict]:
    with session_scope() as session:
        stmt = select(MemoryRecordModel).where(MemoryRecordModel.run_id == run_id).order_by(MemoryRecordModel.created_at.desc())
        records = session.execute(stmt).scalars().all()
        return [
            {
                "id": m.id,
                "run_id": m.run_id,
                "type": m.type,
                "key": m.key,
                "value": m.value_json,
                "source": m.source,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in records
        ]


@app.get("/api/v1/runs/{run_id}/events")
def get_run_events(run_id: str) -> list[dict]:
    with session_scope() as session:
        stmt = select(EventModel).where(EventModel.run_id == run_id).order_by(EventModel.created_at.desc())
        events = session.execute(stmt).scalars().all()
        return [
            {
                "id": e.id,
                "run_id": e.run_id,
                "type": e.type,
                "payload": e.payload,
                "source": e.source,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in events
        ]


@app.get("/api/v1/tasks/{task_id}/patch")
def get_task_patch(task_id: str) -> dict:
    with session_scope() as session:
        stmt = select(TaskArtifactModel).where(TaskArtifactModel.task_id == task_id).order_by(TaskArtifactModel.created_at.desc()).limit(1)
        artifact = session.execute(stmt).scalar_one_or_none()
        if not artifact:
            raise HTTPException(status_code=404, detail="No proposed patch found for this task")
            
        settings = load_settings()
        workspace = Path(settings.project.workspace_path)
        patch_file = workspace / artifact.path
        
        if patch_file.exists():
            patch_content = patch_file.read_text(encoding="utf-8")
        else:
            patch_content = artifact.metadata_json.get("content", "")
            
        if not patch_content:
            raise HTTPException(status_code=404, detail=f"Patch content not found (File exists: {patch_file.exists()})")
            
        return {"task_id": task_id, "path": artifact.path, "content": patch_content}


@app.post("/api/v1/tasks/{task_id}/approve")
def approve_task(task_id: str) -> dict:
    with session_scope() as session:
        task = session.get(TaskModel, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status != "PENDING_APPROVAL":
            raise HTTPException(status_code=400, detail=f"Task is not pending approval (Status: {task.status})")
            
        art_stmt = select(TaskArtifactModel).where(TaskArtifactModel.task_id == task_id).order_by(TaskArtifactModel.created_at.desc()).limit(1)
        artifact = session.execute(art_stmt).scalar_one_or_none()
        if not artifact:
            raise HTTPException(status_code=404, detail="No proposed patch artifact found")
            
        settings = load_settings()
        workspace = Path(settings.project.workspace_path)
        patch_file = workspace / artifact.path
        
        if patch_file.exists():
            patch_content = patch_file.read_text(encoding="utf-8")
        else:
            patch_content = artifact.metadata_json.get("content", "")
            
        if not patch_content:
            raise HTTPException(status_code=404, detail="Patch content not found")
        
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
            
        success = apply_patch(workspace, target_file, patch_content)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to apply patch to workspace")
            
        task.status = "DONE"
        EventRepository(session).publish("REVIEW_COMPLETED", source="api_reviewer", payload={"task_id": task.id, "action": "approved"}, run_id=task.run_id)
        session.commit()
        return {"status": "success", "message": f"Applied patch to {target_file} successfully."}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
