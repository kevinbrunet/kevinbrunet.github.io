#!/usr/bin/env python3
"""Offline retrospective stability check of complement selection, not new rollouts."""
import argparse
import collections
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("oracle", HERE / "analyze-deepswe-oracle.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
LUNA = "mini_swe_agent_gpt_5_6_luna_max"
FLASH = "mini_swe_agent_glm_5_3_flash_max"


def wilson(k, n):
    """Descriptive binomial interval; CV folds do not supply independent trials."""
    z = 1.959963984540054
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [center - half, center + half]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-dir", type=Path, default=Path("analysis/deepswe-oracle/inputs"))
    ap.add_argument("--output-dir", type=Path, default=Path("analysis/deepswe-oracle"))
    args = ap.parse_args()
    task_path = args.input_dir / "tasks.json.gz"
    trial_path = args.input_dir / "trials.json.gz"
    tasks = oracle.load(task_path)["rows"]
    universe = {r["id"] for r in tasks}
    repositories = {r["id"]: r["repository"] for r in tasks}
    assert len(universe) == 113 and len(tasks) == 113
    grouped = collections.defaultdict(lambda: collections.defaultdict(list))
    seen = set()
    for row in oracle.load(trial_path)["rows"]:
        if row["source"] != "deep-swe" or row.get("eval_scope") != "full":
            continue
        assert row["harness"] == "mini-swe-agent" and row["task_name"] in universe
        assert row["trial_name"] not in seen
        seen.add(row["trial_name"])
        oracle.success(row)
        grouped[row["config"]][row["task_name"]].append(row)
    assert len(grouped) == 70
    outcomes = {}
    for config, config_tasks in grouped.items():
        outcomes[config] = {}
        for task in sorted(universe):
            rows = sorted(config_tasks.get(task, []), key=lambda r: (r["started_at"], r["trial_name"]))
            assert len(rows) <= 4
            accepted, cost, attempts, missing_costs = False, 0.0, 0, 0
            for row in rows:
                attempts += 1
                value = oracle.display_cost(row)
                if value is None:
                    missing_costs += 1
                else:
                    cost += value
                if oracle.success(row):
                    accepted = True
                    break
            outcomes[config][task] = dict(accepted=accepted, cost=cost, attempts=attempts,
                                          missing_costs=missing_costs, available=len(rows))
    failures = {t for t in universe if not outcomes[LUNA][t]["accepted"]}
    assert len(failures) == 11
    # Freeze the published article's candidate pool: 66 configurations with complete
    # replay costs on the original residual. This eligibility check is retrospective.
    eligible = sorted(c for c in grouped if all(not outcomes[c][t]["missing_costs"] for t in failures))
    assert len(eligible) == 66

    def rank(training_residual):
        ranked = []
        for config in eligible:
            if config == LUNA:
                continue
            recovered = sum(outcomes[config][t]["accepted"] for t in training_residual)
            cost = sum(outcomes[config][t]["cost"] for t in sorted(training_residual))
            if recovered:
                ranked.append(dict(config=config, recovered=recovered, cost=cost, ratio=cost / recovered))
        # Explicit deterministic tie breaks; never use the held-out task's outcomes.
        return sorted(ranked, key=lambda r: (r["ratio"], -r["recovered"], r["cost"], r["config"]))

    full_ranking = rank(failures)
    assert full_ranking[0]["config"] == FLASH
    fold_sets = {
        "leave_one_task_out": [(t, {t}) for t in sorted(universe)],
        "leave_one_repository_out": [(repo, {t for t in universe if repositories[t] == repo})
                                      for repo in sorted(set(repositories.values()))],
    }
    methods = {}
    for method, folds in fold_sets.items():
        records, selections = [], collections.Counter()
        for fold_id, held_out in folds:
            training_residual = failures - held_out
            ranked = rank(training_residual)
            assert ranked
            best = ranked[0]
            selections[best["config"]] += 1
            for task in sorted(held_out):
                residual = task in failures
                evaluated = outcomes[best["config"]][task]
                records.append(dict(
                    fold=fold_id, task=task, repository=repositories[task],
                    training_tasks=len(universe - held_out), training_residual=len(training_residual),
                    selected=best["config"], training_recovered=best["recovered"],
                    training_cost_per_recovery=best["ratio"],
                    runner_up=ranked[1]["config"], runner_up_ratio=ranked[1]["ratio"],
                    luna_accepted=not residual, complement_invoked=residual,
                    complement_accepted=evaluated["accepted"] if residual else None,
                    complement_cost=evaluated["cost"] if residual else 0,
                    complement_attempts=evaluated["attempts"] if residual else 0,
                    chain_accepted=(not residual) or evaluated["accepted"],
                ))
        assert len(records) == 113 and len({r["task"] for r in records}) == 113
        residual_records = [r for r in records if r["complement_invoked"]]
        recovered = sum(r["complement_accepted"] for r in residual_records)
        assert len(residual_records) == 11
        methods[method] = dict(
            folds=len(folds), selections=dict(selections),
            residual_selections=dict(collections.Counter(r["selected"] for r in residual_records)),
            recovered=recovered, residual_count=11,
            chain_accepted=sum(r["chain_accepted"] for r in records),
            complement_cost=sum(r["complement_cost"] for r in residual_records),
            complement_attempts=sum(r["complement_attempts"] for r in residual_records),
            descriptive_wilson_95=wilson(recovered, 11),
            records=records,
        )
    report = dict(
        purpose="Retrospective selection stability, not prospective validation or oracle qualification",
        fixed_first_model=LUNA, candidate_pool=eligible,
        excluded_cost_incomplete=sorted(set(grouped) - set(eligible)),
        selection_rule="Minimum replay cost / recovered training-residual tasks; ties: more recoveries, lower cost, config id. Zero-recovery candidates excluded. Luna fixed, at most four published attempts, chronological early stop.",
        cost_policy="Same partial repricing as article: Luna x0.2, GLM Flash x0.5, others raw. Estimated costs, not current market prices; oracle costs excluded.",
        limitations=[
            "Luna, objective, candidate pool and analysis selected after examining this dataset.",
            "Candidate eligibility uses cost completeness on all 11 original residual tasks; results on held-out tasks are excluded from fold ranking.",
            "No independent verdicts or new rollouts; missing verdicts are not diagnoses of incorrectness.",
            "Shared training sets, repository dependence and only 11 residual tasks: Wilson is descriptive, not a calibrated generalization interval.",
            "No temporal holdout; repository holdout does not remove all possible cross-repository dependencies.",
        ],
        input_sha256={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (task_path, trial_path)},
        baseline=full_ranking[0], top_five_full_ranking=full_ranking[:5], methods=methods,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "complement-selection.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for method, result in methods.items():
        with (args.output_dir / (method.replace("_", "-") + ".csv")).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(result["records"][0]))
            writer.writeheader()
            writer.writerows(result["records"])
    print(json.dumps({"baseline": full_ranking[:5], "methods": {m: {k: v for k, v in r.items() if k != "records"} for m, r in methods.items()},
                      "residual_tasks": [r for r in methods["leave_one_task_out"]["records"] if r["complement_invoked"]]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
