from __future__ import annotations

import json
import logging
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

logger = logging.getLogger("asep.tools.git")


class GitManager:
    def __init__(self, workspace_path: str | Path) -> None:
        self.workspace_path = Path(workspace_path).resolve()

    def run_git_cmd(self, args: list[str]) -> str:
        """Executes a git command in the workspace path."""
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=str(self.workspace_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: git {' '.join(args)} - Error: {e.stderr.strip()}")
            raise Exception(f"Git command failed: {e.stderr.strip()}")

    def is_git_repository(self) -> bool:
        """Checks if the workspace is a valid Git repository."""
        # Check if the .git directory or file exists, or run git status
        try:
            self.run_git_cmd(["status"])
            return True
        except Exception:
            return False

    def get_current_branch(self) -> str:
        """Returns the current active branch name."""
        return self.run_git_cmd(["branch", "--show-current"])

    def create_and_checkout_branch(self, branch_name: str) -> None:
        """Creates a new branch and checks it out."""
        self.run_git_cmd(["checkout", "-b", branch_name])

    def checkout_branch(self, branch_name: str) -> None:
        """Checks out an existing branch."""
        self.run_git_cmd(["checkout", branch_name])

    def configure_default_user_if_needed(self) -> None:
        """Configures fallback git author if none exists to prevent commit failures."""
        try:
            self.run_git_cmd(["config", "user.name"])
        except Exception:
            logger.info("Git user.name not set. Configuring fallback user.name 'ASEP Agent'.")
            self.run_git_cmd(["config", "user.name", "ASEP Agent"])

        try:
            self.run_git_cmd(["config", "user.email"])
        except Exception:
            logger.info("Git user.email not set. Configuring fallback user.email 'agent@asep.io'.")
            self.run_git_cmd(["config", "user.email", "agent@asep.io"])

    def stage_and_commit(self, files: list[str] | None = None, message: str = "wip") -> None:
        """Stages files and commits them to the current branch."""
        self.configure_default_user_if_needed()
        if files:
            for f in files:
                self.run_git_cmd(["add", f])
        else:
            self.run_git_cmd(["add", "."])
        self.run_git_cmd(["commit", "-m", message])

    def push_branch(self, branch_name: str, remote: str = "origin", force: bool = False) -> None:
        """Pushes the branch to remote repository."""
        args = ["push", remote, branch_name]
        if force:
            args.append("--force")
        self.run_git_cmd(args)


class GitHubClient:
    @staticmethod
    def create_pull_request(
        repo: str,
        head: str,
        base: str,
        title: str,
        body: str,
        token: str
    ) -> str:
        """
        Creates a Pull Request on GitHub.
        Returns:
            pr_url: The HTML URL of the created pull request.
        """
        url = f"https://api.github.com/repos/{repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        
        # Build request with auth headers
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "ASEP-Agent",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("html_url", "")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logger.error(f"GitHub API Error: {e.code} - {err_body}")
            raise Exception(f"Failed to create GitHub PR: {e.code} - {err_body}")
        except Exception as e:
            logger.error(f"Error creating GitHub PR: {e}")
            raise e


def commit_task_patch(workspace_path: str | Path, run_branch: str | None, target_file: str, commit_msg: str) -> None:
    if not run_branch:
        return
    try:
        git_mgr = GitManager(workspace_path)
        git_mgr.checkout_branch(run_branch)
        git_mgr.stage_and_commit(files=[target_file], message=commit_msg)
    except Exception as e:
        logger.error(f"Failed to commit patch to branch {run_branch}: {e}", exc_info=True)

