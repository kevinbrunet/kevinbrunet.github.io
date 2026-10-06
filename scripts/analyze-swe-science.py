#!/usr/bin/env python3
"""Task-level complementarity. Python 3.10+, standard library only; no network.

Official inputs: data/task-matrix.json, data/hard70-model-results.json,
data/benchmark.json, public/traces/*/index.json. Scores only cross-check counts.
Additional independent passes: --runs-manifest (see analysis README).
Missing outcomes are never converted to failures; duplicate trials are rejected.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import re
from collections import defaultdict
from pathlib import Path


ALIASES = {
    "claude-opus-5-max": "opus", "deepseek-v4-pro-max": "deepseek-pro",
    "glm-5-2-max": "glm", "gpt-5-6-sol-max": "gpt",
    "gpt-6-astra-max": "gpt-6-astra", "kimi-k3-max": "kimi",
    "qwen3-8-27b-xhigh": "qwen-3-8-27b",
}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def task_id(value):
    value = str(value).strip()
    match = re.fullmatch(r"(?:task[_-])?(\d+)", value)
    return match[1].zfill(3) if match else value


def binary(value):
    if value is None or value == "":
        raise ValueError("Missing reward, cannot treat as failure")
    number = float(value)
    if number not in (0, 1):
        raise ValueError(f"Non-binary reward: {value!r}")
    return int(number)


def put(outcomes, key, value):
    key = task_id(key)
    if key in outcomes:
        raise ValueError(f"Duplicate task {key}; split independent passes explicitly")
    outcomes[key] = binary(value)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def official_runs(root, classifications, traces_root=None):
    benchmark = read(root / "data/benchmark.json")
    metadata = {m["id"]: m for m in benchmark["models"]}
    matrix = read(root / "data/task-matrix.json")
    universe = [task_id(t["publishedTaskId"]) for t in matrix["tasks"]]
    if len(set(universe)) != len(universe):
        raise ValueError("Duplicate canonical task IDs")
    if len(universe) != benchmark["summary"]["tasks"]:
        raise ValueError("Task count mismatch")
    runs, verification = {}, []
    for model in matrix["models"]:
        mid = model["id"]
        outcomes = {}
        for task in matrix["tasks"]:
            result = task["results"][mid]
            put(outcomes, task["publishedTaskId"], result["reward"])
        runs[mid] = {"run_id": mid, "model": model["family"],
                     "harness": model["harness"], "effort": model["reasoningDepth"],
                     "pass": "selected; original rollout number unpublished",
                     "source": "data/task-matrix.json", "outcomes": outcomes,
                     "open_weight": classifications.get(mid, {}).get("open_weight")}
    supplement = read(root / "data/hard70-model-results.json")
    if supplement["taskCount"] != len(universe):
        raise ValueError("Supplement denominator mismatch")
    for mid, successes in supplement["modelPasses"].items():
        ids = [task_id(t) for t in successes]
        if len(ids) != len(set(ids)) or set(ids) - set(universe):
            raise ValueError(f"Invalid exhaustive success list: {mid}")
        outcomes = {t: int(t in ids) for t in universe}
        if mid in runs:
            if outcomes != runs[mid]["outcomes"]:
                raise ValueError(f"Conflicting supplement for {mid}")
            continue  # Duplicate publication of SAME selection, never another pass.
        m = metadata[mid]
        runs[mid] = {"run_id": mid, "model": m["family"], "harness": m["harness"],
                     "effort": m["reasoningDepth"], "pass": "selected; rollout number unpublished",
                     "source": "data/hard70-model-results.json (exhaustive full-119 success list)",
                     "outcomes": outcomes,
                     "open_weight": classifications.get(mid, {}).get("open_weight")}
    # Aggregate used only as consistency check, never to infer overlaps.
    for mid, run in runs.items():
        score = round(100 * sum(run["outcomes"].values()) / len(universe), 2)
        if score != metadata[mid]["scores"]["overall"]:
            raise ValueError(f"Published aggregate inconsistent with binary tasks: {mid}")
    for index_path in sorted((root / "public/traces").glob("*/index.json")):
        index = read(index_path)
        mid = ALIASES.get(index["experiment"]["id"])
        if mid not in runs:
            raise ValueError(f"Unknown trace configuration {index_path}")
        indexed = {}
        for entry in index["tasks"]:
            tid = task_id(entry["publishedTaskId"])
            put(indexed, tid, entry["evaluation"]["reward"])
            if entry["run"]["harness"] != runs[mid]["harness"]:
                raise ValueError(f"Harness mismatch: {mid} {tid}")
            if traces_root:
                individual_path = traces_root / index_path.parent.name / entry["file"]
                individual = read(individual_path)
                if (task_id(individual["task"]["publishedTaskId"]) != tid
                        or binary(individual["evaluation"]["reward"]) != indexed[tid]
                        or individual["run"] != entry["run"]):
                    raise ValueError(f"Individual trace mismatch: {individual_path}")
        if indexed != runs[mid]["outcomes"]:
            raise ValueError(f"Trace rewards disagree with audited matrix: {mid}")
        verification.append({"run_id": mid, "tasks": len(indexed),
                             "successes": sum(indexed.values()),
                             "individual_traces_checked": bool(traces_root)})
    return runs, universe, verification, metadata


def manifest_runs(path):
    """Explicit metadata prevents guessing model/harness/attempt from paths.

    Formats: csv (task_id,reward), json (rows list), pier (reward.json tree),
    ctrf (only with explicit scoring tests). Relative paths use manifest parent.
    """
    result = {}
    for spec in read(path)["runs"]:
        rid = spec["run_id"]
        if rid in result:
            raise ValueError(f"Duplicate run_id: {rid}")
        source = path.parent / spec["path"]
        outcomes = {}
        fmt = spec["format"]
        if fmt == "csv":
            with source.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        elif fmt == "json":
            obj = read(source)
            rows = obj if isinstance(obj, list) else obj["rows"]
        elif fmt in ("pier", "ctrf"):
            rows = []
            name = "reward.json" if fmt == "pier" else "ctrf.json"
            files = sorted(source.rglob(name))
            if not files:
                raise ValueError(f"No {name} files in {source}")
            for file in files:
                obj = read(file)
                trial_dir = file.parent.parent if file.parent.name == "verifier" else file.parent
                match = re.fullmatch(r"task_(\d{3})(?:__.+)?", trial_dir.name)
                if not match:
                    raise ValueError(f"Cannot identify task: {file}")
                if fmt == "pier":
                    reward = obj["reward"]
                else:
                    # CTRF may mix public/private tests. Never silently score all.
                    scoring = set(spec["scoring_test_names"])
                    tests = [t for t in obj["results"]["tests"] if t["name"] in scoring]
                    if {t["name"] for t in tests} != scoring or not tests:
                        raise ValueError(f"Incomplete CTRF scoring test set: {file}")
                    reward = int(all(t["status"] == "passed" for t in tests))
                rows.append({"task_id": match[1], "reward": reward})
        else:
            raise ValueError(f"Unknown format: {fmt}")
        for row in rows:
            put(outcomes, row[spec.get("task_column", "task_id")],
                row[spec.get("reward_column", "reward")])
        for key in ("model", "harness", "pass", "open_weight"):
            if key not in spec:
                raise ValueError(f"Missing explicit {key} for {rid}")
        result[rid] = {**spec, "source": str(source), "outcomes": outcomes}
    return result


def optimize(runs, successes, slots, only_open=False, reference=None):
    candidates = [k for k, r in runs.items() if not only_open or r["open_weight"] is True]
    best, winners = -1, []
    for combo in itertools.combinations(candidates, slots):
        if reference and reference not in combo:
            continue
        covered = set().union(*(successes[k] for k in combo))
        if len(covered) > best:
            best, winners = len(covered), []
        if len(covered) == best:
            winners.append({"runs": list(combo), "coverage": len(covered),
                            "covered_task_ids": sorted(covered)})
    return {"slots": slots, "coverage": best if best >= 0 else None,
            "optimal_combinations": winners, "available_candidates": len(candidates),
            "interpretation": "retrospective oracle union of distinct published selections"}


def analyze(runs, universe, reference, slots):
    if reference not in runs:
        raise ValueError(f"Reference run missing: {reference}")
    if len(universe) != len(set(universe)):
        raise ValueError("Duplicate universe tasks")
    expected = set(universe)
    for rid, run in runs.items():
        actual = set(run["outcomes"])
        if actual != expected:
            raise ValueError(f"Unequal task scope for {rid}: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    successes = {k: {t for t, v in r["outcomes"].items() if v == 1} for k, r in runs.items()}
    q = successes[reference]
    ranking = []
    for rid, run in runs.items():
        if rid == reference:
            continue
        recovered = successes[rid] - q
        ranking.append({"run_id": rid, "model": run["model"], "harness": run["harness"],
                        "effort": run.get("effort", ""), "open_weight": run["open_weight"],
                        "success_alone": len(successes[rid]), "qwen_recovered": len(recovered),
                        "union": len(q | successes[rid]), "gain": len(recovered),
                        "gain_percentage_points": 100 * len(recovered) / len(universe),
                        "recovered_task_ids": sorted(recovered)})
    ranking.sort(key=lambda r: (-r["qwen_recovered"], r["run_id"]))
    groups = defaultdict(list)
    for rid, run in runs.items():
        groups[(run["model"], run["harness"], run.get("effort", ""))].append(rid)
    passes = []
    for (model, harness, effort), ids in groups.items():
        passes.append({"model": model, "harness": harness, "effort": effort,
                       "observed_selections": len(ids),
                       "per_selection": [{"run_id": k, "pass": runs[k]["pass"],
                                          "successes": len(successes[k])} for k in ids],
                       "observed_union": len(set().union(*(successes[k] for k in ids))),
                       "best_observed_four": optimize({k: runs[k] for k in ids}, successes, 4) if len(ids) >= 4 else None})
    homogeneous = next(g["best_observed_four"] for g in passes
                       if reference in [s["run_id"] for s in g["per_selection"]])
    return {"reference": {k: v for k, v in runs[reference].items() if k != "outcomes"},
            "task_count": len(universe), "reference_successes": len(q),
            "reference_failures": sorted(expected - q), "ranking": ranking,
            "best_open_weight": next((r for r in ranking if r["open_weight"] is True), None),
            "passes": passes, "homogeneous_four": homogeneous,
            "best_four_open": optimize(runs, successes, slots, only_open=True),
            "best_four_open_with_reference": optimize(runs, successes, slots, only_open=True, reference=reference),
            "best_four_all": optimize(runs, successes, slots),
            "best_four_all_with_reference": optimize(runs, successes, slots, reference=reference)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--official-dir", type=Path)
    parser.add_argument("--traces-root", type=Path, help="Optional directory of full per-task trace files to verify")
    parser.add_argument("--classifications", type=Path,
                        default=Path("analysis/swe-bench-science/model-classifications.json"))
    parser.add_argument("--runs-manifest", type=Path)
    parser.add_argument("--reference", default="qwen-3-8-27b")
    parser.add_argument("--slots", type=int, default=4)
    parser.add_argument("--output", type=Path, default=Path("analysis/swe-bench-science/results"))
    args = parser.parse_args()
    if args.slots < 1:
        parser.error("--slots must be positive")
    runs, universe, verification, metadata = {}, [], [], {}
    if args.official_dir:
        runs, universe, verification, metadata = official_runs(
            args.official_dir, read(args.classifications), args.traces_root)
    if args.runs_manifest:
        extra = manifest_runs(args.runs_manifest)
        if set(extra) & set(runs):
            raise ValueError("Additional runs duplicate published run IDs")
        runs.update(extra)
        if not universe:
            universe = sorted(runs[args.reference]["outcomes"])
    if not runs:
        parser.error("Provide --official-dir and/or --runs-manifest")
    report = analyze(runs, universe, args.reference, args.slots)
    report["input_sha256"] = {
        str(p.relative_to(args.official_dir)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(args.official_dir.rglob("*")) if p.is_file()
    } if args.official_dir else {}
    report["verification"] = verification
    report["classification_sha256"] = hashlib.sha256(args.classifications.read_bytes()).hexdigest() if args.official_dir else None
    report["runs_manifest_sha256"] = hashlib.sha256(args.runs_manifest.read_bytes()).hexdigest() if args.runs_manifest else None
    report["excluded_published_configurations"] = [m for mid, m in metadata.items() if mid not in runs]
    args.output.mkdir(parents=True, exist_ok=True)
    write_json(args.output / "analysis.json", report)
    ids = list(runs)
    write_csv(args.output / "task-model-matrix.csv", ["task_id", *ids],
              [{"task_id": t, **{k: runs[k]["outcomes"][t] for k in ids}} for t in sorted(universe)])
    fields = ["run_id", "model", "harness", "effort", "open_weight", "success_alone",
              "qwen_recovered", "union", "gain", "gain_percentage_points"]
    write_csv(args.output / "complementarity.csv", fields,
              [{k: row[k] for k in fields} for row in report["ranking"]])
    write_csv(args.output / "recovered-tasks.csv", ["run_id", "task_id"],
              [{"run_id": r["run_id"], "task_id": t} for r in report["ranking"] for t in r["recovered_task_ids"]])
    write_csv(args.output / "reference-failures.csv", ["task_id"],
              [{"task_id": t} for t in report["reference_failures"]])
    print(json.dumps({"N": len(universe), "reference_successes": report["reference_successes"],
                      "best_open_weight": report["best_open_weight"],
                      "four_open": report["best_four_open"]["coverage"],
                      "four_with_reference": report["best_four_open_with_reference"]["coverage"],
                      "homogeneous_four": report["homogeneous_four"]}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
