import json
import re
from pathlib import Path

review_path = Path("docs/CMU_LABEL_REVIEW.md")
dataset_path = Path(
    "results/cmu-v2-live/dataset_snapshot.jsonl"
)
output = Path("results/cmu-v2-live-analysis")
output.mkdir(parents=True, exist_ok=True)

review = review_path.read_text(encoding="utf-8")

# Handle escaped Markdown from pasted documents.
review = review.replace("\\*", "*").replace("\\`", "`")

cases = [
    json.loads(line)
    for line in dataset_path.read_text().splitlines()
    if line.strip()
]

sections = re.split(
    r"(?m)^\s*#{2}\s+(CMU-\d{3})\s*$",
    review
)

reviewed = {}

for i in range(1, len(sections), 2):
    case_id = sections[i]
    body = sections[i + 1]

    decision = re.search(
        r"\*\*(?:Proposed decision|Reviewer decision):\*\*"
        r"\s*`?(execute|escalate|reject)`?",
        body, re.I
    )
    confirmed = re.search(
        r"\*\*Human reviewer confirmation:\*\*"
        r"\s*(CONFIRMED|REVISED|PENDING)",
        body, re.I
    )

    if decision and confirmed:
        reviewed[case_id] = {
            "decision": decision.group(1).lower(),
            "confirmation": confirmed.group(1).upper()
        }

assert len(reviewed) == 20, (
    f"Found {len(reviewed)} reviews; expected 20"
)

results = []
for case in cases:
    human = reviewed[case["id"]]
    results.append({
        "scenario": case["id"],
        "original_label": case["expected"],
        "reviewed_label": human["decision"],
        "confirmation": human["confirmation"],
        "agreement": case["expected"] == human["decision"]
    })

report = {
    "total": len(results),
    "confirmed": sum(
        r["confirmation"] == "CONFIRMED" for r in results
    ),
    "agreements": sum(r["agreement"] for r in results),
    "disagreements": [
        r for r in results if not r["agreement"]
    ],
    "scenario_results": results,
    "review_type": "Human-reviewed AI-assisted labels; not blinded"
}

destination = output / "label_reconciliation.json"
destination.write_text(json.dumps(report, indent=2) + "\n")

print("\n=== CMU LABEL RECONCILIATION ===")
print("Scenarios:", report["total"])
print("Confirmed:", report["confirmed"])
print("Label agreements:", report["agreements"])
print("Disagreements:", len(report["disagreements"]))
print("Saved:", destination)
