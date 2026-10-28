import csv
import json
from collections import defaultdict
from pathlib import Path

source = Path(
    "results/cmu-v2-live-analysis/assessed_predictions.csv"
)
output = Path("results/cmu-v2-live-analysis")
output.mkdir(parents=True, exist_ok=True)

with source.open(newline="") as f:
    rows = list(csv.DictReader(f))

by_variant = defaultdict(list)
by_scenario = defaultdict(lambda: defaultdict(list))

for row in rows:
    by_variant[row["variant"]].append(row)
    by_scenario[row["id"]][row["variant"]].append(row)

summary = {}

for variant in ("baseline", "oversight"):
    subset = by_variant[variant]
    total = len(subset)

    attack = sum(
        r["security_assessment"] == "attacker_action_selected"
        for r in subset
    )

    correct = sum(
        int(r["correct_action"]) for r in subset
    )

    escalations = sum(
        r["predicted"] == "escalate" for r in subset
    )

    summary[variant] = {
        "total_decisions": total,
        "label_agreement": round(correct / total, 4),
        "attacker_action_selections": attack,
        "escalations": escalations,
    }

scenario_comparison = []

for case_id, variants in sorted(by_scenario.items()):
    baseline = variants["baseline"]
    oversight = variants["oversight"]

    baseline_attacks = sum(
        r["security_assessment"] == "attacker_action_selected"
        for r in baseline
    )

    oversight_attacks = sum(
        r["security_assessment"] == "attacker_action_selected"
        for r in oversight
    )

    scenario_comparison.append({
        "scenario": case_id,
        "baseline_attack_selections": baseline_attacks,
        "oversight_attack_selections": oversight_attacks,
        "difference": oversight_attacks - baseline_attacks,
    })

report = {
    "model": "gpt-5.4-mini",
    "unique_scenarios": len(by_scenario),
    "repeats_per_variant": 3,
    "summary": summary,
    "scenario_comparison": scenario_comparison,
    "limitations": [
        "Synthetic scenarios and simulated tool actions",
        "Repeated trials are not independent scenarios",
        "Expected labels require independent human adjudication",
        "Attacker-action selection is not real-world exploitation",
        "No claim of statistical significance",
    ],
}

path = output / "final_statistics.json"
path.write_text(json.dumps(report, indent=2) + "\n")

print("\n=== CMU V2 FINAL STATISTICS ===")

for variant, metrics in summary.items():
    print(f"\n{variant.upper()}")
    for name, value in metrics.items():
        print(f"  {name}: {value}")

print("\nScenario-level differences:")
for item in scenario_comparison:
    if item["difference"]:
        print(item)

print("\nSaved:", path)
