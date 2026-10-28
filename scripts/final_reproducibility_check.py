import csv
import hashlib
import json
from pathlib import Path

checks = []

def check(name, result):
    checks.append((name, bool(result)))
    print(("PASS" if result else "FAIL"), name)

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

required_files = [
    "data/scenarios_v2.jsonl",
    "data/stress_scenarios.jsonl",
    "data/cmu_security_holdout_v2.jsonl",
    "data/cmu_security_policy_v2.json",
    "docs/RESEARCH_FINDINGS.md",
    "docs/CMU_010_CASE_STUDY.md",
    "docs/CMU_LABEL_REVIEW.md",
    "results/cmu-v2-live/dataset_snapshot.jsonl",
    "results/cmu-v2-live/policy_snapshot.json",
    "results/cmu-v2-live/live_predictions.csv",
    "results/cmu-v2-live-analysis/assessed_predictions.csv",
    "results/cmu-v2-live-analysis/label_reconciliation.json",
]

for filename in required_files:
    check(f"File exists: {filename}", Path(filename).is_file())

dataset = Path("results/cmu-v2-live/dataset_snapshot.jsonl")
source_dataset = Path("data/cmu_security_holdout_v2.jsonl")
policy = Path("results/cmu-v2-live/policy_snapshot.json")
source_policy = Path("data/cmu_security_policy_v2.json")

if dataset.exists() and source_dataset.exists():
    check(
        "Dataset snapshot matches source",
        sha256(dataset) == sha256(source_dataset)
    )

if policy.exists() and source_policy.exists():
    check(
        "Policy snapshot matches source",
        sha256(policy) == sha256(source_policy)
    )

predictions_path = Path(
    "results/cmu-v2-live/live_predictions.csv"
)

if predictions_path.exists():
    with predictions_path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    check("120 model decisions", len(rows) == 120)
    check(
        "20 unique scenarios",
        len({r["id"] for r in rows}) == 20
    )
    check(
        "60 baseline decisions",
        sum(r["variant"] == "baseline" for r in rows) == 60
    )
    check(
        "60 oversight decisions",
        sum(r["variant"] == "oversight" for r in rows) == 60
    )

reconciliation_path = Path(
    "results/cmu-v2-live-analysis/label_reconciliation.json"
)

if reconciliation_path.exists():
    reconciliation = json.loads(
        reconciliation_path.read_text()
    )
    check(
        "20 confirmed labels",
        reconciliation["confirmed"] == 20
    )
    check(
        "20 label agreements",
        reconciliation["agreements"] == 20
    )

print("\n=== FINAL REPRODUCIBILITY AUDIT ===")
passed = sum(result for _, result in checks)
print(f"Passed: {passed}/{len(checks)}")

if passed != len(checks):
    raise SystemExit("AUDIT FAILED")

print("All local artifact consistency checks passed.")
