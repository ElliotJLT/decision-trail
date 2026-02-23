"""Git operations for decision-trail."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def is_git_repo(path: Path) -> bool:
    """Check if path is inside a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=path,
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def git_add_and_commit(filepath: Path, message: str) -> Optional[str]:
    """Stage a file and commit it. Returns the commit hash or None on failure."""
    repo_root = filepath.parent
    # Walk up to find the git root
    while repo_root != repo_root.parent:
        if (repo_root / ".git").exists():
            break
        repo_root = repo_root.parent
    else:
        return None

    try:
        subprocess.run(
            ["git", "add", str(filepath)],
            cwd=repo_root,
            capture_output=True,
            check=True,
        )
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_root,
            capture_output=True,
            check=True,
            text=True,
        )
        # Extract short hash
        hash_result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            check=True,
            text=True,
        )
        return hash_result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def git_add_and_commit_multiple(filepaths: list[Path], message: str) -> Optional[str]:
    """Stage multiple files and commit. Returns the commit hash or None."""
    if not filepaths:
        return None

    repo_root = filepaths[0].parent
    while repo_root != repo_root.parent:
        if (repo_root / ".git").exists():
            break
        repo_root = repo_root.parent
    else:
        return None

    try:
        for fp in filepaths:
            subprocess.run(
                ["git", "add", str(fp)],
                cwd=repo_root,
                capture_output=True,
                check=True,
            )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_root,
            capture_output=True,
            check=True,
            text=True,
        )
        hash_result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            check=True,
            text=True,
        )
        return hash_result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
