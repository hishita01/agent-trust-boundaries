import csv
from collections import defaultdict
from pathlib import Path

source = Path(
    "results/cmu-reanalysis-v2/cmu_audited_predictions.csv"
)
destination = Path(
    "results/cmu-reanalysis-v2/security_review.md"
)

with source.open(newline="") as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(list)

for row in rows:
    groups[row["id"]].append(row)

lines = [
    "# CMU Security Evaluation — Manual Review",
    "",
    "## Methodology",
    "",
    "Model-generated decisions are evaluated separately",
    "from the original benchmark's action-label agreement.",
    "No external tools were executed.",
    "",
]

for case_id, records in sorted(groups.items()):
    lines.extend([
        f"## {case_id}",
        "",
        "| Trial | Variant | Decision | Tool | Target |",
        "|---|---|---|---|---|",
    ])

    for r in records:
        lines.append(
            f"| {r['trial']} | {r['variant']} | "
            f"{r['predicted']} | {r['tool']} | "
            f"{r['target']} |"
        )

    lines.extend([
        "",
        "### Security assessment",
        "",
        "Pending independent authorization and",
        "attacker-objective review.",
        "",
        "### Model reasoning",
        "",
    ])

    for r in records:
        lines.extend([
            f"**{r['variant']} — trial {r['trial']}**",
            "",
            r["reason"].replace("\n", " "),
            "",
        ])

destination.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("Security review created:")
print(destination)
print("Scenarios:", len(groups))
print("Decisions:", len(rows))
