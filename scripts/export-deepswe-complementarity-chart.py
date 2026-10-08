#!/usr/bin/env python3
"""Export the compact dataset used by the reusable scatter-chart shortcode."""

import argparse
import collections
import gzip
import json
import pathlib


DISPLAY_NAMES = {
    "claude": "Claude",
    "deepseek": "DeepSeek",
    "gemini": "Gemini",
    "glm": "GLM",
    "gpt": "GPT",
    "grok": "Grok",
    "kimi": "Kimi",
    "luna": "Luna",
    "astra": "Astra",
    "opus": "Opus",
    "sonnet": "Sonnet",
    "fable": "Fable",
    "flash": "Flash",
    "pro": "Pro",
    "code": "Code",
}


def model_label(value):
    if value.startswith("gpt-"):
        parts = value.split("-")
        version = ".".join(part for part in parts[1:] if part.isdigit())
        suffix = " ".join(
            DISPLAY_NAMES.get(part, part.capitalize())
            for part in parts[1:]
            if not part.isdigit()
        )
        return f"GPT-{version}{f' {suffix}' if suffix else ''}"
    if value.startswith("glm-"):
        parts = value.split("-")
        version = ".".join(part for part in parts[1:] if part.isdigit())
        suffix = " ".join(
            DISPLAY_NAMES.get(part, part.capitalize())
            for part in parts[1:]
            if not part.isdigit()
        )
        return f"GLM-{version}{f' {suffix}' if suffix else ''}"
    parts = value.split("-")
    rendered = []
    for part in parts:
        if part.isdigit() and rendered and rendered[-1][-1:].isdigit():
            rendered[-1] += f".{part}"
        elif part.isdigit():
            rendered.append(part)
        else:
            rendered.append(DISPLAY_NAMES.get(part, part.capitalize()))
    return " ".join(rendered)


def load_json(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def repriced_cost(row):
    factor = {"gpt-5-6-luna": 0.2, "glm-5-3-flash": 0.5}.get(row["model"], 1)
    return None if row["cost_usd"] is None else row["cost_usd"] * factor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=pathlib.Path("analysis/deepswe-oracle/analysis.json"),
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("data/charts/deepswe-luna-cost-recovery.json"),
    )
    parser.add_argument(
        "--trials",
        type=pathlib.Path,
        default=pathlib.Path("analysis/deepswe-oracle/inputs/trials.json.gz"),
    )
    parser.add_argument(
        "--routing-output",
        type=pathlib.Path,
        default=pathlib.Path("data/charts/deepswe-routing-orders.json"),
    )
    parser.add_argument(
        "--budget-output",
        type=pathlib.Path,
        default=pathlib.Path("data/charts/deepswe-luna-astra-budget.json"),
    )
    args = parser.parse_args()

    report = json.loads(args.input.read_text(encoding="utf-8"))
    luna_failures = set(report["luna_failures"])
    grouped = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in load_json(args.trials)["rows"]:
        if (
            row["source"] == "deep-swe"
            and row.get("eval_scope") == "full"
            and row["task_name"] in luna_failures
        ):
            grouped[row["config"]][row["task_name"]].append(row)
    for tasks in grouped.values():
        for trials in tasks.values():
            trials.sort(key=lambda row: (row["started_at"], row["trial_name"]))

    points = []
    for metric in report["metrics"]:
        attempts = 0
        cost = 0.0
        missing_costs = 0
        for task in sorted(luna_failures):
            for row in grouped[metric["config"]].get(task, []):
                attempts += 1
                value = repriced_cost(row)
                if value is None:
                    missing_costs += 1
                else:
                    cost += value
                if row["passed"]:
                    break
        points.append(
            {
                "id": metric["config"],
                "label": f'{model_label(metric["model"])} [{metric["effort"]}]',
                "x": round(cost, 6),
                "y": metric["luna_failures_recovered"],
                "attempts": attempts,
                "missing_costs": missing_costs,
            }
        )

    incomplete = [point for point in points if point["missing_costs"]]
    points = [point for point in points if not point["missing_costs"]]
    points.sort(key=lambda point: (point["x"], point["y"], point["label"]))
    output = {
        "source": [
            "analysis/deepswe-oracle/analysis.json",
            "analysis/deepswe-oracle/inputs/trials.json.gz",
        ],
        "retrieved_at": report["retrieved_at"],
        "point_count": len(points),
        "excluded_incomplete_costs": [point["id"] for point in incomplete],
        "cost_policy": report["cost_policy"],
        "points": points,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    routing = {
        "source": "analysis/deepswe-oracle/analysis.json",
        "retrieved_at": report["retrieved_at"],
        "point_count": 2,
        "routes": [
            {
                "id": "glm-first",
                "label_fr": "GLM Flash en premier",
                "label_en": "GLM Flash first",
                "cost": round(report["flash_luna_glm_replay"]["cost_usd_repriced"], 6),
                "coverage": report["task_count"] - len(report["flash_luna_glm_replay"]["remaining_tasks"]),
                "attempts": report["flash_luna_glm_replay"]["attempts"],
            },
            {
                "id": "luna-first",
                "label_fr": "Luna en premier",
                "label_en": "Luna first",
                "cost": round(report["luna_flash_glm_replay"]["cost_usd_repriced"], 6),
                "coverage": report["task_count"] - len(report["luna_flash_glm_replay"]["remaining_tasks"]),
                "attempts": report["luna_flash_glm_replay"]["attempts"],
            },
        ],
    }
    args.routing_output.parent.mkdir(parents=True, exist_ok=True)
    args.routing_output.write_text(
        json.dumps(routing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    metrics_by_config = {metric["config"]: metric for metric in report["metrics"]}
    luna = metrics_by_config["mini_swe_agent_gpt_5_6_luna_max"]
    astra = metrics_by_config["mini_swe_agent_gpt_6_astra_xhigh"]
    budget = {
        "source": "analysis/deepswe-oracle/analysis.json",
        "retrieved_at": report["retrieved_at"],
        "point_count": 2,
        "routes": [
            {
                "id": "luna-four",
                "label_fr": "Luna, quatre essais",
                "label_en": "Luna, four attempts",
                "cost": round(luna["mean_cost_usd_repriced"] * 4, 6),
                "coverage": round(luna["observed_up_to_four_union"] / report["task_count"] * 100, 1),
                "attempts": 4,
            },
            {
                "id": "astra-one",
                "label_fr": "Astra, un essai",
                "label_en": "Astra, one attempt",
                "cost": round(astra["mean_cost_usd_repriced"], 6),
                "coverage": round(astra["mean_single_trial_pass_rate"] * 100, 1),
                "attempts": 1,
            },
        ],
    }
    args.budget_output.parent.mkdir(parents=True, exist_ok=True)
    args.budget_output.write_text(
        json.dumps(budget, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
