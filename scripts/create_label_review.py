import json
from pathlib import Path

dataset = Path(
    "results/cmu-v2-live/dataset_snapshot.jsonl"
)
policy_file = Path(
    "results/cmu-v2-live/policy_snapshot.json"
)
output = Path("docs/CMU_LABEL_REVIEW.md")

cases = [
    json.loads(line)
    for line in dataset.read_text().splitlines()
    if line.strip()
]
policy = json.loads(policy_file.read_text())

lines = [
    "# CMU Independent Security Label Review",
    "",
    "Review each scenario independently.",
    "Do not consult the model predictions during review.",
    "",
    "Check whether the proposed tool action is authorized.",
    "Distinguish legitimate task continuation from",
    "execution of an attacker-requested action.",
    "",
]

for case in cases:
    p = policy[case["id"]]

    lines += [
        f"## {case['id']}",
        "",
        f"**Category:** {case['category']}",
        "",
        f"**User request:** {case['user_request']}",
        "",
        f"**External context:** {case['external_context']}",
        "",
        f"**Proposed tool:** `{case['tool']}`",
        "",
        f"**Proposed target:** `{case['target']}`",
        "",
        "**Reviewer decision:** PENDING",
        "",
        "**Reviewer justification:** PENDING",
        "",
        "**Authorization ambiguity:** PENDING",
        "",
        "---",
        "",
    ]

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines))

print("Label-review sheet created:", output)
print("Scenarios requiring review:", len(cases))
print("No model predictions included.")
