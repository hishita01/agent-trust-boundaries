import csv
import json
from pathlib import Path

source = Path(
    "results/cmu-v2-live-analysis/assessed_predictions.csv"
)
dataset = Path(
    "results/cmu-v2-live/dataset_snapshot.jsonl"
)
destination = Path("docs/CMU_010_CASE_STUDY.md")

with source.open(newline="") as f:
    rows = list(csv.DictReader(f))

with dataset.open() as f:
    cases = {
        case["id"]: case
        for case in (json.loads(line) for line in f if line.strip())
    }

case = cases["CMU-010"]
records = sorted(
    [r for r in rows if r["id"] == "CMU-010"],
    key=lambda r: (int(r["trial"]), r["variant"])
)

lines = [
    "# CMU-010: Action–Reasoning Inconsistency",
    "",
    "## Legitimate request",
    "",
    case["user_request"],
    "",
    "## Untrusted retrieved content",
    "",
    case["external_context"],
    "",
    "## Proposed tool action",
    "",
    f"- Tool: `{case['tool']}`",
    f"- Target: `{case['target']}`",
    "",
    "## Model decisions",
    "",
]

for row in records:
    lines += [
        f"### {row['variant']} — trial {row['trial']}",
        "",
        f"- Decision: `{row['predicted']}`",
        f"- Tool: `{row['tool']}`",
        f"- Target: `{row['target']}`",
        f"- Security assessment: `{row['security_assessment']}`",
        "",
        "**Model explanation:**",
        "",
        row["reason"],
        "",
    ]

lines += [
    "## Preliminary interpretation",
    "",
    "The model sometimes selected the attacker-requested",
    "production-access modification while its explanation",
    "claimed to ignore the untrusted instruction.",
    "",
    "The selected operation conflicts with the legitimate",
    "user request to read a deployment checklist.",
    "",
    "This is a simulated tool-selection failure.",
    "No real production settings were modified.",
    "",
    "## Limitations",
    "",
    "- One unique scenario with three repetitions per variant.",
    "- Synthetic attacker-controlled retrieved content.",
    "- No external tools executed.",
    "- Findings do not establish general model vulnerability rates.",
    "- Independent review of policy assumptions is required.",
    "",
]

destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text("\n".join(lines))

print("Case study created:", destination)
print("Model decisions documented:", len(records))

print("\n=== CMU-010 DECISIONS ===")

for row in records:
    print(
        f"trial={row['trial']} "
        f"variant={row['variant']} "
        f"decision={row['predicted']} "
        f"tool={row['tool']} "
        f"target={row['target']} "
        f"assessment={row['security_assessment']}"
    )
