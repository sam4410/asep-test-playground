from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from asep.tools.workspace import apply_patch

class Sandbox:
    def __init__(self, workspace_path: str | Path, sandbox_type: str = "local") -> None:
        self.workspace_path = Path(workspace_path).resolve()
        self.sandbox_type = sandbox_type

    def run_validation(self, patch_content: str, test_cmd: str = "pytest") -> tuple[bool, str]:
        """
        Creates a sandboxed copy of the workspace, parses and applies the patch, and runs the validation command.
        Returns:
            (success: bool, stdout_and_stderr: str)
        """
        target_file = self.extract_target_file(patch_content)
        
        # Create temp dir
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_path = Path(temp_dir_name)
            
            # Copy workspace files excluding ignored directories to keep copy fast
            ignored_dirs = {".git", "__pycache__", ".asep", ".venv", ".ruff_cache", "node_modules", "venv", "env"}
            
            for item in os.listdir(self.workspace_path):
                s = self.workspace_path / item
                d = temp_path / item
                if item in ignored_dirs:
                    continue
                if s.is_dir():
                    shutil.copytree(s, d, symlinks=True, ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.venv', '.git', '.asep', '.ruff_cache'))
                else:
                    shutil.copy2(s, d)
            
            # Apply the patch in the temporary workspace
            if patch_content and target_file:
                try:
                    apply_success = apply_patch(temp_path, target_file, patch_content)
                    if not apply_success:
                        return False, "Failed to apply patch in sandbox environment."
                except Exception as e:
                    return False, f"Error applying patch in sandbox: {e}"
            
            # Run the test/validation command inside temporary workspace
            try:
                env = os.environ.copy()
                res = subprocess.run(
                    test_cmd,
                    shell=True,
                    cwd=str(temp_path),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=60,  # 1 minute execution limit
                    env=env
                )
                return res.returncode == 0, res.stdout
            except subprocess.TimeoutExpired as e:
                return False, f"Sandbox validation command timed out. Output so far:\n{e.output}"
            except Exception as e:
                return False, f"Sandbox execution error: {e}"

    @staticmethod
    def extract_target_file(patch_content: str) -> str:
        """Helper to extract target file from unified diff header."""
        for line in patch_content.splitlines():
            if line.startswith("+++ b/"):
                return line[6:].strip()
            elif line.startswith("+++ "):
                return line[4:].strip()
        return ""
