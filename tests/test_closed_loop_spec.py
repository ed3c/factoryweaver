import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs/closed-loop-v72/project.json"
CLI = ROOT / "scripts/factoryweaver.py"
REQUIREMENTS = [
    "REQ-intent", "REQ-coverage", "REQ-dependencies", "REQ-spec-data",
    "REQ-stable-update", "REQ-correction", "REQ-identity", "REQ-events",
    "REQ-schema", "REQ-test", "REQ-hook", "REQ-cron", "REQ-inner-loop",
    "REQ-outer-loop", "REQ-manager-feedback", "REQ-consumption",
    "REQ-completion", "REQ-invalidation", "REQ-replay", "REQ-unknown-effect",
    "REQ-retry-budget", "REQ-thinking-router", "REQ-ponytail",
    "REQ-eval-evidence", "REQ-compiler-audit", "REQ-adapters", "REQ-safety",
    "REQ-handoff", "REQ-cost", "REQ-publication",
]


class ClosedLoopSpecTests(unittest.TestCase):
    def invoke(self, action, record=None):
        with tempfile.TemporaryDirectory() as directory:
            input_path = PROJECT
            if record is not None:
                input_path = Path(directory) / "project.json"
                input_path.write_text(json.dumps(record), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CLI), action, str(input_path)],
                capture_output=True, text=True,
            )

    def test_original_denominator_is_preserved_without_completion(self):
        result = self.invoke("project")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual([r["requirement"] for r in output["projection"]], REQUIREMENTS)
        self.assertEqual(output["completion"], "COMPILED_ONLY")
        self.assertEqual(output["operation_scope"], "READ_ONLY_NO_EXECUTION")
        self.assertTrue(all(not r["authorizes_effects"] for r in output["projection"]))
        self.assertTrue(all(r["engineering"] == "UNASSESSED" for r in output["projection"]))

    def test_unknown_hook_blocks_its_consumers_and_keeps_other_work(self):
        record = json.loads(PROJECT.read_text())
        hook = next(r for r in record["requirements"] if r["id"] == "REQ-hook")
        hook["knowledge_status"] = "UNKNOWN"
        result = self.invoke("project", record)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = {r["requirement"]: r for r in json.loads(result.stdout)["projection"]}
        self.assertEqual(list(rows), REQUIREMENTS)
        self.assertEqual(rows["REQ-hook"]["state"], "WAIT_FOR_EVIDENCE")
        self.assertEqual(rows["REQ-manager-feedback"]["state"], "WAIT_FOR_PREREQUISITE")
        self.assertIn("REQ-hook", rows["REQ-manager-feedback"]["missing"])
        self.assertEqual(rows["REQ-consumption"]["state"], "WAIT_FOR_PREREQUISITE")
        self.assertEqual(rows["REQ-test"]["state"], "READY_FOR_OWNER_REVIEW")
        self.assertEqual(rows["REQ-thinking-router"]["state"], "READY_FOR_OWNER_REVIEW")

    def test_false_activation_is_refused(self):
        record = json.loads(PROJECT.read_text())
        record["requirements"][0]["engineering_status"] = "ACTIVATED"
        result = self.invoke("validate", record)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["error"], "untrusted_test_claim:REQ-intent")

    def test_cyclic_original_requirements_are_refused(self):
        record = json.loads(PROJECT.read_text())
        record["requirements"][0]["depends_on"] = ["REQ-coverage"]
        result = self.invoke("project", record)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["error"], "requirement_dependency_cycle:REQ-intent")


if __name__ == "__main__":
    unittest.main()
