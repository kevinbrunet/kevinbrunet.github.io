"""Meaningful safeguards for complementarity, missing data and rollout identity."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location("science", Path(__file__).with_name("analyze-swe-science.py"))
science = importlib.util.module_from_spec(spec)
spec.loader.exec_module(science)


def run(model, outcomes, pass_number=1):
    return {"model": model, "harness": "test", "pass": pass_number,
            "open_weight": True, "outcomes": outcomes}


class AnalysisTests(unittest.TestCase):
    def test_complement_is_not_global_score(self):
        runs = {"q": run("Q", {"001": 1, "002": 1, "003": 1, "004": 0}),
                "high": run("High", {"001": 1, "002": 1, "003": 1, "004": 0}),
                "low": run("Low", {"001": 0, "002": 0, "003": 0, "004": 1})}
        result = science.analyze(runs, list(runs["q"]["outcomes"]), "q", 2)
        self.assertEqual(result["best_open_weight"]["run_id"], "low")
        self.assertEqual(result["best_open_weight"]["union"], 4)

    def test_missing_is_not_failure(self):
        with self.assertRaises(ValueError):
            science.binary("")
        with self.assertRaises(ValueError):
            science.analyze({"q": run("Q", {"001": 1}), "x": run("X", {})}, ["001"], "q", 2)

    def test_duplicate_trials_rejected(self):
        outcomes = {}
        science.put(outcomes, "task_001", 0)
        with self.assertRaises(ValueError):
            science.put(outcomes, "001", 1)

    def test_fractional_reward_rejected(self):
        with self.assertRaises(ValueError):
            science.binary(0.75)

    def test_four_distinct_passes_preserved(self):
        runs = {f"q{i}": run("Q", {str(j): int(i == j) for j in range(4)}, i + 1) for i in range(4)}
        result = science.analyze(runs, list("0123"), "q0", 4)
        self.assertEqual(result["homogeneous_four"]["coverage"], 4)
        self.assertEqual(len(result["passes"][0]["per_selection"]), 4)
        one = science.analyze({"q0": runs["q0"]}, list("0123"), "q0", 4)
        self.assertIsNone(one["homogeneous_four"])
        self.assertIsNone(one["best_four_open"]["coverage"])

    def test_optimizer_returns_all_ties_and_excludes_proprietary(self):
        runs = {"a": run("A", {}), "b": run("B", {}), "c": run("C", {}),
                "closed": {**run("Closed", {}), "open_weight": False}}
        successes = {"a": {"1"}, "b": {"2"}, "c": {"2"}, "closed": {"1", "2", "3"}}
        result = science.optimize(runs, successes, 2, only_open=True, reference="a")
        self.assertEqual(result["coverage"], 2)
        self.assertEqual(len(result["optimal_combinations"]), 2)

    def test_manifest_csv_and_reward_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "pass1.csv").write_text("task_id,reward\n001,0\n002,1\n", encoding="utf-8")
            verifier = root / "pass2/task_001__trial/verifier"
            verifier.mkdir(parents=True)
            (verifier / "reward.json").write_text('{"reward":1}', encoding="utf-8")
            manifest = {"runs": [{"run_id": "q1", "model": "Q", "harness": "A", "pass": 1,
                                    "open_weight": True, "format": "csv", "path": "pass1.csv"},
                                   {"run_id": "q2", "model": "Q", "harness": "B", "pass": 2,
                                    "open_weight": True, "format": "pier", "path": "pass2"}]}
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            parsed = science.manifest_runs(path)
            self.assertEqual(parsed["q1"]["outcomes"], {"001": 0, "002": 1})
            self.assertEqual(parsed["q2"]["outcomes"], {"001": 1})
            self.assertNotEqual(parsed["q1"]["harness"], parsed["q2"]["harness"])


if __name__ == "__main__":
    unittest.main()
