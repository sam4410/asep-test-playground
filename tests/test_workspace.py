from __future__ import annotations

import tempfile
from pathlib import Path
from asep.tools.workspace import list_files, read_file, write_file, search_files, detect_project, apply_patch

def test_workspace_file_operations():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Write file
        write_file(tmp_path, "app/main.py", "def run():\n    print('start')\n")
        
        # Read file
        assert read_file(tmp_path, "app/main.py") == "def run():\n    print('start')\n"
        
        # List files
        files = list_files(tmp_path)
        assert files == ["app/main.py"]
        
        # Search files
        matches = search_files(tmp_path, "start")
        assert len(matches) == 1
        assert matches[0]["path"] == "app/main.py"
        assert matches[0]["line"] == 2
        assert matches[0]["content"] == "print('start')"

def test_detect_project():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        write_file(tmp_path, "pyproject.toml", "[tool.ruff]\n")
        write_file(tmp_path, "alembic.ini", "script_location = migrations\n")
        
        info = detect_project(tmp_path)
        assert info["language"] == "Python"
        assert info["migrations"] == "Alembic"

def test_apply_patch_modify():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        write_file(tmp_path, "hello.py", "print('hello')\nprint('world')\n")
        
        patch = (
            "--- a/hello.py\n"
            "+++ b/hello.py\n"
            "@@ -1,2 +1,2 @@\n"
            " print('hello')\n"
            "-print('world')\n"
            "+print('everyone')\n"
        )
        
        success = apply_patch(tmp_path, "hello.py", patch)
        assert success is True
        assert read_file(tmp_path, "hello.py") == "print('hello')\nprint('everyone')\n"

def test_apply_patch_create():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        patch = (
            "--- /dev/null\n"
            "+++ b/new_file.py\n"
            "@@ -0,0 +1,2 @@\n"
            "+# New file\n"
            "+print('created')\n"
        )
        
        success = apply_patch(tmp_path, "new_file.py", patch)
        assert success is True
        assert read_file(tmp_path, "new_file.py") == "# New file\nprint('created')\n"
