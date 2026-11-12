"""Read task contracts and evaluate their checks using only reviewed argv forms."""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
TASK_ID = re.compile(r"T[0-9]{2}|DEMO")
TEST_TARGET = re.compile(r"tests(?:\.[A-Za-z_][A-Za-z_0-9]*)+")
STATUSES = {"planned", "todo", "ready", "in_progress", "blocked", "in_review", "done"}
TOOLS = {"git", "java", "mvn", "hdfs", "spark-submit"}
PATH_FIELDS = ("input_files", "output_files")
CHECK_FIELDS = ("input_checks", "output_checks", "merge_checks")
REQUIRED = {
    "id", "title", "phase", "status", "priority", "assignee", "workstream",
    "estimated_scope", "dependencies", "merge_dependencies", "acceptance",
    *PATH_FIELDS, *CHECK_FIELDS,
}
OPTIONAL = {"csv_headers", "input_tools", "output_tools"}


class InvalidContract(ValueError):
    """The repository's task metadata is malformed."""


class Blocked(RuntimeError):
    """A prerequisite is unavailable."""


def repo_path(root, name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise InvalidContract(f"Expected a relative POSIX path: {name!r}")
    parts = PurePosixPath(name).parts
    if not parts or any(part in {".", "..", "/"} or part.casefold() == ".git" for part in parts):
        raise InvalidContract(f"Unsafe path: {name!r}")
    resolved = root.joinpath(*parts).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise InvalidContract(f"Path resolves outside the repo: {name!r}")
    return resolved


def load_toml(root, name):
    try:
        return tomllib.loads(repo_path(root, name).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InvalidContract(f"{name}: {exc}") from exc


def string_list(value, field, required=False):
    if not isinstance(value, list) or (required and not value):
        raise InvalidContract(f"{field} must be a {'nonempty ' if required else ''}list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise InvalidContract(f"{field} entries must be nonempty strings")
    if len(set(value)) != len(value):
        raise InvalidContract(f"{field} contains a duplicate")
    return value


def validate_task(root, task_id, task):
    if REQUIRED.difference(task) or set(task).difference(REQUIRED | OPTIONAL):
        raise InvalidContract(f"{task_id}: task fields do not match the schema")
    if task["id"] != task_id:
        raise InvalidContract(f"{task_id}: contract ID differs from registry")
    for field in ("title", "phase", "priority", "assignee", "workstream", "estimated_scope"):
        if not isinstance(task[field], str) or not task[field].strip():
            raise InvalidContract(f"{task_id}: missing {field}")
    if not isinstance(task["status"], str) or task["status"] not in STATUSES:
        raise InvalidContract(f"{task_id}: invalid status")
    for field in ("dependencies", "merge_dependencies", "acceptance"):
        string_list(task[field], field, required=field == "acceptance")
    for field in PATH_FIELDS:
        for name in string_list(task[field], field, required=True):
            repo_path(root, name)
    for field in CHECK_FIELDS:
        checks = task[field]
        if not isinstance(checks, list) or not checks:
            raise InvalidContract(f"{task_id}: {field} must contain at least one check")
        for check in checks:
            if (not isinstance(check, list) or len(check) != 4
                    or check[:3] != ["python", "-m", "unittest"]
                    or not isinstance(check[3], str) or not TEST_TARGET.fullmatch(check[3])):
                raise InvalidContract(f"{task_id}: unsupported command in {field}: {check!r}")
    for field in ("input_tools", "output_tools"):
        for tool in string_list(task.get(field, []), field):
            if tool not in TOOLS:
                raise InvalidContract(f"{task_id}: unsupported tool {tool!r}")
    headers = task.get("csv_headers", {})
    if not isinstance(headers, dict):
        raise InvalidContract(f"{task_id}: csv_headers must be a table")
    for name, columns in headers.items():
        if name not in task["input_files"]:
            raise InvalidContract(f"{task_id}: {name} must be an input to check its header")
        string_list(columns, f"{name} columns", required=True)


def load_registry(root=ROOT):
    registry = load_toml(root, "tasks/registry.toml")
    if set(registry) != {"task_ids"}:
        raise InvalidContract("registry.toml must contain only task_ids")
    task_ids = string_list(registry["task_ids"], "task_ids", required=True)
    tasks = {}
    for task_id in task_ids:
        if not TASK_ID.fullmatch(task_id):
            raise InvalidContract(f"Invalid task ID: {task_id!r}")
        task = load_toml(root, f"tasks/{task_id}/task.toml")
        validate_task(root, task_id, task)
        tasks[task_id] = task

    visiting = set()
    visited = set()

    def visit(task_id):
        if task_id in visiting:
            raise InvalidContract(f"Dependency cycle through {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        task = tasks[task_id]
        for parent in task["dependencies"] + task["merge_dependencies"]:
            if parent not in tasks:
                raise InvalidContract(f"{task_id} depends on unknown task {parent!r}")
            visit(parent)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in task_ids:
        visit(task_id)
    return tasks


def review_dependency(root, tasks, task_id):
    if task_id not in tasks or tasks[task_id]["status"] != "done":
        raise Blocked(f"Dependency {task_id} needs reviewed completion")
    path = f"tasks/{task_id}/review.toml"
    if not repo_path(root, path).is_file():
        raise Blocked(f"Dependency {task_id} needs {path}")
    review = load_toml(root, path)
    for field in ("reviewed_by", "commit", "evidence"):
        value = review.get(field)
        if not isinstance(value, str) or not value.strip():
            raise Blocked(f"Dependency {task_id} has incomplete review evidence")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", review["commit"]):
        raise Blocked(f"Dependency {task_id} has an invalid review commit")
    if not repo_path(root, review["evidence"]).is_file():
        raise Blocked(f"Dependency {task_id} evidence file is missing")
    for name in tasks[task_id]["output_files"]:
        if not repo_path(root, name).is_file():
            raise Blocked(f"Dependency {task_id} is missing delivered output {name}")


def check_files(root, files):
    missing = [name for name in files if not repo_path(root, name).is_file()]
    if missing:
        raise Blocked(f"Missing required files: {', '.join(missing)}")


def check_headers(root, headers):
    for name, expected in headers.items():
        with repo_path(root, name).open(encoding="utf-8-sig", newline="") as source:
            actual = next(csv.reader(source), [])
        if actual != expected:
            raise InvalidContract(f"{name} header: expected {expected}, got {actual}")


def check_tools(tools):
    missing = [name for name in tools if not shutil.which(name)]
    if missing:
        raise Blocked(f"Missing executable(s): {', '.join(missing)}")


def run_checks(root, checks, results):
    for argv in checks:
        module = argv[3].split(".")
        candidates = ["/".join(module[:length]) + ".py" for length in range(2, len(module) + 1)]
        if not any(repo_path(root, candidate).is_file() for candidate in candidates):
            raise Blocked(f"Planned test module for {argv[3]} is missing")
        result = subprocess.run([sys.executable, "-B", *argv[1:]], cwd=root)
        results.append({"argv": argv, "exit_code": result.returncode})
        if result.returncode:
            raise InvalidContract(f"Check exited {result.returncode}: {' '.join(argv)}")


def perform(root, tasks, task_id, kind, results):
    if task_id not in tasks:
        raise InvalidContract(f"Unknown task {task_id!r}")
    task = tasks[task_id]
    if kind == "input":
        for parent in task["dependencies"]:
            review_dependency(root, tasks, parent)
        check_files(root, task["input_files"])
        check_headers(root, task.get("csv_headers", {}))
        check_tools(task.get("input_tools", []))
    elif kind == "output":
        check_files(root, task["output_files"])
        check_tools(task.get("output_tools", []))
    run_checks(root, task[f"{kind}_checks"], results)


def git_revision(root):
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "rev-parse", "--verify", "HEAD"],
            cwd=root, capture_output=True, text=True,
        )
    except FileNotFoundError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def task_cli(kind):
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    args = parser.parse_args()
    if not TASK_ID.fullmatch(args.task):
        parser.error("expected a Txx task ID or DEMO")
    results = []
    code, state, detail = 0, "PASS", "All required checks passed"
    try:
        perform(ROOT, load_registry(), args.task, kind, results)
    except Blocked as exc:
        code, state, detail = 2, "BLOCKED", str(exc)
    except (ValueError, OSError) as exc:
        code, state, detail = 1, "FAIL", str(exc)
    if kind == "output":
        try:
            path = repo_path(ROOT, f"artifacts/quality/{args.task}/output.json")
            path.parent.mkdir(parents=True, exist_ok=True)
            evidence = {
                "task": args.task, "status": state, "detail": detail,
                "timestamp": datetime.now(timezone.utc).isoformat(), "commit": git_revision(ROOT),
                "checks": results,
            }
            path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except (OSError, ValueError) as exc:
            code, state, detail = 1, "FAIL", f"Could not write output evidence: {exc}"
    print(f"{state} {args.task} {kind}: {detail}")
    return code
