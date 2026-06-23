from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from asep.agents.base import AgentContext
from asep.agents.debugging import SelfHealingAgent
from asep.tools.sandbox import Sandbox

def test_sandbox_extract_target_file():
    patch_content = (
        "--- a/asep/api/main.py\n"
        "+++ b/asep/api/main.py\n"
        "@@ -15,4 +15,9 @@"
    )
    target = Sandbox.extract_target_file(patch_content)
    assert target == "asep/api/main.py"

def test_sandbox_run_validation_success(tmp_path):
    # Setup a mock workspace
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    # Create a dummy file
    code_file = workspace / "math_utils.py"
    code_file.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    
    # Create a test file
    test_file = workspace / "test_math.py"
    test_file.write_text("from math_utils import add\ndef test_add():\n    assert add(2, 3) == 5\n", encoding="utf-8")
    
    # Sandbox runner
    sandbox = Sandbox(workspace_path=workspace)
    
    # Apply a correct patch
    patch_content = (
        "--- a/math_utils.py\n"
        "+++ b/math_utils.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a + b\n"
        "+    return a + b + 0\n"
    )
    
    success, output = sandbox.run_validation(patch_content, test_cmd="python -m pytest test_math.py")
    assert success is True
    assert "passed" in output.lower()

def test_sandbox_run_validation_failure(tmp_path):
    # Setup a mock workspace
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    # Create a dummy file
    code_file = workspace / "math_utils.py"
    code_file.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    
    # Create a test file
    test_file = workspace / "test_math.py"
    test_file.write_text("from math_utils import add\ndef test_add():\n    assert add(2, 3) == 5\n", encoding="utf-8")
    
    # Sandbox runner
    sandbox = Sandbox(workspace_path=workspace)
    
    # Apply a broken patch (asserting 2 + 3 == 6)
    patch_content = (
        "--- a/math_utils.py\n"
        "+++ b/math_utils.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a + b\n"
        "+    return a + b + 1\n"
    )
    
    success, output = sandbox.run_validation(patch_content, test_cmd="python -m pytest test_math.py")
    assert success is False
    assert "failed" in output.lower()

@patch("asep.llm.LLMClient")
def test_self_healing_agent_success(mock_llm_class, tmp_path):
    # Setup a mock workspace
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    code_file = workspace / "math_utils.py"
    code_file.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    
    test_file = workspace / "test_math.py"
    test_file.write_text("from math_utils import add\ndef test_add():\n    assert add(2, 3) == 5\n", encoding="utf-8")
    
    # The first patch is broken (adds 1 to result)
    broken_patch = (
        "--- a/math_utils.py\n"
        "+++ b/math_utils.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a + b\n"
        "+    return a + b + 1\n"
    )
    
    # The healed patch fixes it
    healed_patch = (
        "--- a/math_utils.py\n"
        "+++ b/math_utils.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a + b\n"
        "+    return a + b\n"
    )
    
    # Mock LLM generation
    mock_llm_instance = MagicMock()
    mock_llm_instance.generate.return_value = f"```diff\n{healed_patch}\n```"
    mock_llm_class.return_value = mock_llm_instance
    
    context = AgentContext(
        run_id=None,
        goal="Fix addition",
        workspace_path=str(workspace)
    )
    
    healer = SelfHealingAgent()
    success, final_patch, report = healer.heal_task(
        context=context,
        original_patch=broken_patch,
        test_cmd="python -m pytest test_math.py",
        max_attempts=2
    )
    
    assert success is True
    assert "PASSED" in report
    assert "math_utils.py" in final_patch
    mock_llm_instance.generate.assert_called_once()
