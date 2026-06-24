from __future__ import annotations

import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from asep.tools.git import GitManager, GitHubClient, commit_task_patch


def test_git_manager_is_repository():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="On branch main\n", returncode=0)
        mgr = GitManager("/fake/path")
        
        assert mgr.is_git_repository() is True
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0] == ["git", "status"]


def test_git_manager_is_not_repository():
    import subprocess
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(128, ["git", "status"], stderr="not a git repository")
        mgr = GitManager("/fake/path")
        
        assert mgr.is_git_repository() is False


def test_git_manager_create_and_checkout_branch():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", returncode=0)
        mgr = GitManager("/fake/path")
        
        mgr.create_and_checkout_branch("test-branch")
        assert mock_run.call_args[0][0] == ["git", "checkout", "-b", "test-branch"]


def test_git_manager_stage_and_commit():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", returncode=0)
        mgr = GitManager("/fake/path")
        
        mgr.stage_and_commit(files=["file1.py", "file2.py"], message="fix: bugs")
        
        # Check configure fallback user calls + git add calls + git commit
        calls = [c[0][0] for c in mock_run.call_args_list]
        assert ["git", "add", "file1.py"] in calls
        assert ["git", "add", "file2.py"] in calls
        assert ["git", "commit", "-m", "fix: bugs"] in calls


def test_git_manager_push():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", returncode=0)
        mgr = GitManager("/fake/path")
        
        mgr.push_branch("test-branch", remote="origin", force=True)
        assert mock_run.call_args[0][0] == ["git", "push", "origin", "test-branch", "--force"]


def test_github_client_create_pr_success():
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"html_url": "https://github.com/owner/repo/pull/42"}'
    
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        url = GitHubClient.create_pull_request(
            repo="owner/repo",
            head="feature-branch",
            base="main",
            title="ASEP PR",
            body="Descriptions",
            token="gh_token_123"
        )
        
        assert url == "https://github.com/owner/repo/pull/42"
        
        # Verify request parameters
        req_arg = mock_urlopen.call_args[0][0]
        assert req_arg.full_url == "https://api.github.com/repos/owner/repo/pulls"
        assert req_arg.headers["Authorization"] == "token gh_token_123"
        assert req_arg.method == "POST"


def test_github_client_create_pr_failure():
    mock_fp = MagicMock()
    mock_fp.read.return_value = b'{"message": "Validation Failed"}'
    
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/owner/repo/pulls",
            code=422,
            msg="Unprocessable Entity",
            hdrs=None,
            fp=mock_fp
        )
        
        with pytest.raises(Exception) as exc_info:
            GitHubClient.create_pull_request(
                repo="owner/repo",
                head="feature-branch",
                base="main",
                title="ASEP PR",
                body="Descriptions",
                token="gh_token_123"
            )
            
        assert "Failed to create GitHub PR: 422" in str(exc_info.value)


def test_commit_task_patch_helper():
    with patch("asep.tools.git.GitManager") as mock_git_mgr_cls:
        mock_git_mgr = MagicMock()
        mock_git_mgr_cls.return_value = mock_git_mgr
        
        commit_task_patch(
            workspace_path="/fake/path",
            run_branch="asep/run-12345",
            target_file="asep/db/models.py",
            commit_msg="feat: database updates"
        )
        
        mock_git_mgr.checkout_branch.assert_called_once_with("asep/run-12345")
        mock_git_mgr.stage_and_commit.assert_called_once_with(
            files=["asep/db/models.py"],
            message="feat: database updates"
        )
