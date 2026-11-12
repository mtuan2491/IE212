import csv
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/tasks"))
sys.path.insert(0, str(ROOT / "src"))
import gate
from ie212_instacart import bootstrap_demo


class FixtureTests(unittest.TestCase):
    def test_fixture_deduplicates_and_counts_per_order(self):
        self.assertEqual(bootstrap_demo.count_pairs(bootstrap_demo.FIXTURE), {(3, 7): 2, (3, 9): 1})

    def test_headers_and_full_output(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "pairs.csv"
            bootstrap_demo.write_counts(destination=destination)
            with destination.open(encoding="utf-8", newline="") as handle:
                self.assertEqual(list(csv.reader(handle)), [
                    ["product_a", "product_b", "count"],
                    ["3", "7", "2"],
                    ["3", "9", "1"],
                ])


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.contract = (ROOT / "tasks/DEMO/task.toml").read_text(encoding="utf-8")

    def write(self, path, contents):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")

    def registry(self, demo=None, parent=None):
        ids = '["DEMO"]' if parent is None else '["DEMO", "T01"]'
        self.write("tasks/registry.toml", f"task_ids = {ids}")
        self.write("tasks/DEMO/task.toml", self.contract if demo is None else demo)
        if parent is not None:
            self.write("tasks/T01/task.toml", parent.replace('id = "DEMO"', 'id = "T01"'))

    def test_valid_registry(self):
        self.registry(parent=self.contract)
        self.assertEqual(set(gate.load_registry(self.root)), {"DEMO", "T01"})

    def test_rejects_three_digit_task_id(self):
        self.registry()
        self.write("tasks/registry.toml", 'task_ids = ["T001"]')
        with self.assertRaisesRegex(gate.InvalidContract, "Invalid task ID"):
            gate.load_registry(self.root)

    def test_malformed_toml(self):
        self.registry("title = [")
        with self.assertRaisesRegex(gate.InvalidContract, "task.toml"):
            gate.load_registry(self.root)

    def test_missing_dependency_definition(self):
        self.registry(self.contract.replace("dependencies = []", 'dependencies = ["T01"]', 1))
        with self.assertRaisesRegex(gate.InvalidContract, "unknown task"):
            gate.load_registry(self.root)

    def test_dependency_cycle(self):
        demo = self.contract.replace("dependencies = []", 'dependencies = ["T01"]', 1)
        parent = self.contract.replace("merge_dependencies = []", 'merge_dependencies = ["DEMO"]', 1)
        self.registry(demo, parent)
        with self.assertRaisesRegex(gate.InvalidContract, "Dependency cycle"):
            gate.load_registry(self.root)

    def test_pending_dependency(self):
        demo = self.contract.replace("dependencies = []", 'dependencies = ["T01"]', 1)
        self.registry(demo, self.contract.replace('status = "ready"', 'status = "planned"'))
        with self.assertRaisesRegex(gate.Blocked, "reviewed completion"):
            gate.perform(self.root, gate.load_registry(self.root), "DEMO", "input", [])

    def test_missing_output(self):
        self.registry()
        with self.assertRaisesRegex(gate.Blocked, "Missing required files"):
            gate.perform(self.root, gate.load_registry(self.root), "DEMO", "output", [])

    def test_failed_check_propagates(self):
        self.registry()
        self.write("tests/test_bootstrap.py", "")
        completed = subprocess.CompletedProcess([], 1)
        results = []
        with patch.object(gate.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(gate.InvalidContract, "exited 1"):
                gate.run_checks(self.root, [["python", "-m", "unittest", "tests.test_bootstrap"]], results)
        self.assertEqual(results[0]["exit_code"], 1)

    def test_rejects_path_traversal_and_unsafe_argv(self):
        for path in ("../raw.csv", "C:/raw.csv", "/tmp/raw.csv", ".git/config"):
            with self.subTest(path=path), self.assertRaises(gate.InvalidContract):
                gate.repo_path(self.root, path)
        self.registry(self.contract.replace('"python","-m","unittest"', '"bash", "-c", "anything"', 1))
        with self.assertRaisesRegex(gate.InvalidContract, "unsupported command"):
            gate.load_registry(self.root)

    def test_header_mismatch(self):
        self.registry()
        self.write("tests/fixtures/baskets.csv", "wrong,product_id\n")
        with self.assertRaisesRegex(gate.InvalidContract, "header"):
            gate.perform(self.root, gate.load_registry(self.root), "DEMO", "input", [])

    def test_missing_hdfs_is_blocked(self):
        with patch.object(gate.shutil, "which", return_value=None):
            with self.assertRaisesRegex(gate.Blocked, "hdfs"):
                gate.check_tools(["hdfs"])


class MergeTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("validate_merge", ROOT / "scripts/ci/validate_merge.py")
        self.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.validator)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--initial-branch=main")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "user.name=IE212 fixture", "-c", "user.email=fixture@example.invalid", *args],
            cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout.strip()

    def commit(self, contents):
        (self.root / "file.txt").write_text(contents + "\n", encoding="utf-8")
        self.git("add", "file.txt")
        self.git("commit", "-m", contents)

    def test_missing_base_blocks(self):
        with self.assertRaisesRegex(gate.Blocked, "Missing commit"):
            self.validator.merge(self.root, "main", None)

    def test_merge_conflict_keeps_refs_and_worktree(self):
        self.commit("base")
        self.git("branch", "feature")
        self.commit("main changed")
        self.git("switch", "feature")
        self.commit("feature changed")
        target, feature = self.git("rev-parse", "main"), self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(gate.InvalidContract, "Merge conflict"):
            self.validator.merge(self.root, "main", None)
        self.assertEqual(self.git("rev-parse", "main"), target)
        self.assertEqual(self.git("rev-parse", "HEAD"), feature)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual((self.root / "file.txt").read_text(encoding="utf-8").strip(), "feature changed")
