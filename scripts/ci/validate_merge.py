"""Check the tentative merge in a disposable snapshot. Leave refs and the worktree alone."""
import argparse
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/tasks"))
from gate import Blocked, InvalidContract, TASK_ID, load_registry, perform, repo_path, review_dependency


def git(root, *args):
    try:
        return subprocess.run(
            ["git", "--no-optional-locks", *args], cwd=root, capture_output=True, text=True,
        )
    except FileNotFoundError as exc:
        raise Blocked("Git is unavailable") from exc


def revision(root, ref):
    result = git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    if result.returncode:
        raise Blocked(f"Missing commit for {ref!r}")
    return result.stdout.strip()


def snapshot(root, revision_id, folder):
    bundle = folder.with_suffix(".zip")
    result = git(root, "archive", "--format=zip", f"--output={bundle}", revision_id)
    if result.returncode:
        raise InvalidContract(result.stderr.strip())
    folder.mkdir()
    with zipfile.ZipFile(bundle) as archive:
        for entry in archive.infolist():
            repo_path(folder, entry.filename)
        archive.extractall(folder)


def merge(root, base, task_id):
    target, head = revision(root, base), revision(root, "HEAD")
    status = git(root, "status", "--porcelain=v1", "--untracked-files=normal")
    if status.returncode:
        raise InvalidContract(status.stderr.strip())
    if status.stdout:
        raise Blocked("Commit the task changes before checking the merge snapshot")
    if git(root, "merge-base", target, head).returncode:
        raise Blocked("Base and HEAD have no common history")
    diff = git(root, "diff", "--check", f"{target}...{head}")
    if diff.returncode:
        raise InvalidContract((diff.stdout or diff.stderr).strip())
    tree = git(root, "merge-tree", "--write-tree", "--name-only", target, head)
    if tree.returncode == 1:
        raise InvalidContract(f"Merge conflict\n{tree.stdout.strip()}")
    if tree.returncode:
        raise Blocked(f"Could not compute a merge tree: {tree.stderr.strip()}")
    tree_id = tree.stdout.splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="ie212-merge-") as temp:
        folder = Path(temp)
        candidate = folder / "candidate"
        snapshot(root, tree_id, candidate)
        tasks = load_registry(candidate)
        if task_id:
            if task_id not in tasks:
                raise InvalidContract(f"Unknown task {task_id!r}")
            task = tasks[task_id]
            dependencies = task["dependencies"] + task["merge_dependencies"]
            if dependencies:
                base_snapshot = folder / "base"
                snapshot(root, target, base_snapshot)
                base_tasks = load_registry(base_snapshot)
                for parent in dict.fromkeys(dependencies):
                    review_dependency(base_snapshot, base_tasks, parent)
                    if tasks[parent] != base_tasks[parent]:
                        raise Blocked(f"Dependency contract {parent} differs from the base")
                    for name in base_tasks[parent]["output_files"] + [f"tasks/{parent}/review.toml"]:
                        if repo_path(candidate, name).read_bytes() != repo_path(base_snapshot, name).read_bytes():
                            raise Blocked(f"Dependency output {name} differs from the base")
            perform(candidate, tasks, task_id, "merge", [])
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        subprocess.run([sys.executable, "scripts/tasks/validate_contracts.py"], cwd=candidate, env=env, check=True)
        subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
            cwd=candidate, env=env, check=True,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base", nargs="?", default="main")
    parser.add_argument("task", nargs="?")
    args = parser.parse_args()
    if args.task and not TASK_ID.fullmatch(args.task):
        parser.error("expected a Txx task ID or DEMO")
    try:
        merge(ROOT, args.base, args.task)
    except Blocked as exc:
        print(f"BLOCKED merge: {exc}")
        return 2
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print(f"FAIL merge: {exc}")
        return 1
    print(f"PASS merge against {args.base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
