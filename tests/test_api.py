from __future__ import annotations

import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from asep.api.main import app
from asep.db.session import session_scope
from asep.db.models import RunModel, TaskModel, TaskArtifactModel
from asep.domain import TaskStatus
from asep.repositories import RunRepository, TaskRepository

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_projects_endpoint():
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "ASEP Platform"


def test_create_and_get_run_workflow():
    # 1. Create run
    response = client.post("/api/v1/runs", json={"requirement": "Design a schema and write code"})
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["status"] == "PLANNED"
    
    run_id = data["run_id"]
    
    # 2. Get run details
    response = client.get(f"/api/v1/runs/{run_id}")
    assert response.status_code == 200
    run_data = response.json()
    assert run_data["id"] == run_id
    assert "Design a schema" in run_data["goal"]
    assert run_data["status"] == "PLANNED"
    
    # 3. Get runs list
    response = client.get("/api/v1/runs")
    assert response.status_code == 200
    runs = response.json()
    assert len(runs) >= 1
    assert any(r["id"] == run_id for r in runs)
    
    # 4. Get run tasks
    response = client.get(f"/api/v1/runs/{run_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0
    # Requirement task is first, Architect inspect is second
    assert tasks[0]["owner"] == "product_manager"
    assert tasks[1]["owner"] == "architect"
    
    # 5. Get run memory
    response = client.get(f"/api/v1/runs/{run_id}/memory")
    assert response.status_code == 200
    memory = response.json()
    assert len(memory) >= 2  # requirement spec and plan graph
    assert any(m["key"] == "requirement_spec" for m in memory)
    assert any(m["key"] == "plan_graph" for m in memory)
    
    # 6. Get run events
    response = client.get(f"/api/v1/runs/{run_id}/events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 2
    assert any(e["type"] == "REQUIREMENT_PARSED" for e in events)
    assert any(e["type"] == "PLAN_CREATED" for e in events)


def test_approve_task_endpoint():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Override workspace path temporarily for testing patch application
        from unittest.mock import patch
        
        # Write dummy file to workspace
        target_file_path = tmp_path / "hello.py"
        target_file_path.write_text("print('hello')\n", encoding="utf-8")
        
        # Propose patch
        patch_content = (
            "--- a/hello.py\n"
            "+++ b/hello.py\n"
            "@@ -1,1 +1,2 @@\n"
            " print('hello')\n"
            "+print('dashboard UI')\n"
        )
        
        # Create artifacts folder structure
        artifacts_dir = tmp_path / ".asep" / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        patch_file = artifacts_dir / "test_patch.diff"
        patch_file.write_text(patch_content, encoding="utf-8")
        
        with session_scope() as session:
            run_repo = RunRepository(session)
            task_repo = TaskRepository(session)
            
            run = run_repo.create(goal="Goal")
            
            # Create task pending approval
            from asep.domain import Task
            t = Task(title="Test Task", description="Desc", owner="coding_agent")
            task_row = task_repo.add_task(run.id, t)
            task_row.status = "PENDING_APPROVAL"
            session.flush()
            
            # Save task artifact path relative to workspace
            session.add(TaskArtifactModel(
                task_id=task_row.id,
                path=".asep/artifacts/test_patch.diff",
                kind="diff",
                metadata_json={}
            ))
            session.commit()
            
            task_id = task_row.id
        
        # 1. Fetch patch endpoint
        # Mock load_settings to return workspace path pointing to our temp directory
        from asep.config import FileConfig
        mock_config = FileConfig()
        mock_config.project.workspace_path = tmp_path
        
        with patch("asep.api.main.load_settings", return_value=mock_config), \
             patch("asep.tools.workspace.apply_patch", wraps=lambda w, tf, p: True) as mock_apply:
            
            response = client.get(f"/api/v1/tasks/{task_id}/patch")
            assert response.status_code == 200
            assert response.json()["content"] == patch_content
            
            # 2. Approve endpoint
            response = client.post(f"/api/v1/tasks/{task_id}/approve")
            assert response.status_code == 200
            assert response.json()["status"] == "success"
            
        # Verify status updated to DONE
        with session_scope() as session:
            session.expire_all()
            task_row = session.get(TaskModel, task_id)
            assert task_row.status == "DONE"
