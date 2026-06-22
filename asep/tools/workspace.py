from __future__ import annotations

import os
from pathlib import Path

def list_files(workspace_path: str | Path) -> list[str]:
    """Recursively list all files in the workspace, excluding ignored patterns."""
    root = Path(workspace_path).resolve()
    ignored_dirs = {".git", "__pycache__", ".asep", ".venv", ".ruff_cache", "node_modules", "venv", "env"}
    ignored_files = {".env", ".gitignore", "pyproject.toml", "alembic.ini", "asep.yaml"}

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        path = Path(dirpath)
        # Prune ignored directories
        if any(ignored in path.parts for ignored in ignored_dirs):
            continue
        
        # Remove ignored directories in-place so os.walk doesn't traverse them
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]

        for f in filenames:
            if f in ignored_files:
                continue
            rel_path = path.relative_to(root) / f
            files.append(str(rel_path.as_posix()))
            
    return sorted(files)

def read_file(workspace_path: str | Path, rel_path: str) -> str:
    """Read file content safely."""
    full_path = Path(workspace_path).resolve() / rel_path
    if not full_path.resolve().is_relative_to(Path(workspace_path).resolve()):
        raise ValueError("Path traversal attempt detected.")
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {rel_path}")
    return full_path.read_text(encoding="utf-8")

def search_files(workspace_path: str | Path, query: str) -> list[dict[str, str | int]]:
    """Search for query string across workspace files."""
    root = Path(workspace_path).resolve()
    files = list_files(root)
    results = []

    for f_path in files:
        full_path = root / f_path
        try:
            content = full_path.read_text(encoding="utf-8")
            if query in content:
                for line_idx, line in enumerate(content.splitlines(), 1):
                    if query in line:
                        results.append({
                            "path": f_path,
                            "line": line_idx,
                            "content": line.strip()
                        })
        except Exception:
            # Skip unreadable or binary files
            continue
            
    return results

def detect_project(workspace_path: str | Path) -> dict[str, str]:
    """Detect project characteristics, languages, and frameworks."""
    root = Path(workspace_path).resolve()
    characteristics = {}

    if (root / "pyproject.toml").exists() or (root / "setup.py").exists() or (root / "requirements.txt").exists():
        characteristics["language"] = "Python"
    elif (root / "package.json").exists():
        characteristics["language"] = "NodeJS"
    else:
        characteristics["language"] = "Unknown"
        
    if (root / "alembic.ini").exists():
        characteristics["migrations"] = "Alembic"
        
    return characteristics

def write_file(workspace_path: str | Path, rel_path: str, content: str) -> None:
    """Write contents to a file safely, creating directories if needed."""
    full_path = Path(workspace_path).resolve() / rel_path
    if not full_path.resolve().parent.is_relative_to(Path(workspace_path).resolve()):
        raise ValueError("Path traversal attempt detected.")
    
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")

def apply_patch(workspace_path: str | Path, file_path: str, patch_content: str) -> bool:
    """Parse and apply a unified diff to a file in the workspace."""
    root = Path(workspace_path).resolve()
    full_path = root / file_path
    if not full_path.resolve().is_relative_to(root):
        raise ValueError("Path traversal attempt detected.")

    original_content = ""
    if full_path.exists():
        original_content = full_path.read_text(encoding="utf-8")

    lines = original_content.splitlines(keepends=True)
    patch_lines = patch_content.splitlines(keepends=True)

    hunks = []
    current_hunk = None

    for pline in patch_lines:
        if pline.startswith("@@"):
            # Parse hunk header: @@ -old_start,old_len +new_start,new_len @@
            try:
                header = pline.split("@@")[1].strip()
                old_part, new_part = header.split(" ")
                old_start_str = old_part.split(",")[0].replace("-", "")
                old_start = int(old_start_str)
                old_len = int(old_part.split(",")[1]) if "," in old_part else 1
                
                hunks.append({
                    "old_start": old_start,
                    "old_len": old_len,
                    "changes": []
                })
                current_hunk = hunks[-1]
            except Exception:
                continue
        elif current_hunk is not None:
            if pline.startswith("\\") or pline.startswith("---") or pline.startswith("+++"):
                continue
            current_hunk["changes"].append(pline)

    if not hunks:
        # If no hunks detected, treat patch_content as direct file overwrite
        write_file(root, file_path, patch_content)
        return True

    # Sort hunks from bottom to top of the file to keep line indices stable
    hunks.sort(key=lambda h: h["old_start"], reverse=True)

    for hunk in hunks:
        start_idx = hunk["old_start"] - 1  # convert to 0-indexed
        old_len = hunk["old_len"]
        
        hunk_added = []
        for change in hunk["changes"]:
            if change.startswith("-"):
                # Line to delete - skip adding
                continue
            elif change.startswith("+"):
                # Line to add
                hunk_added.append(change[1:])
            elif change.startswith(" "):
                # Context line - keep
                hunk_added.append(change[1:])

        # Apply the hunk
        # If the file is brand new, start_idx might be -1 or 0; handle carefully
        if start_idx < 0:
            start_idx = 0
            
        lines[start_idx:start_idx + old_len] = hunk_added

    new_content = "".join(lines)
    write_file(root, file_path, new_content)
    return True
