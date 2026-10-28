import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from src.security_scoring import assess_security


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predictions",
        default="results/cmu-v2-toy/toy_demo_predictions.csv"
    )
    parser.add_argument(
        "--policy",
        default="data/cmu_security_policy_v2.json"
    )
    parser.add_argument(
        "--out",
        default="results/cmu-v2-analysis"
    )
    args = parser.parse_args()

    policy = json.loads(Path(args.policy).read_text())

    with Path(args.predictions).open(newline="") as f:
        rows = list(csv.DictReader(f))

    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)

    assessed = []

    for row in rows:
        case_id = row["id"]

        if case_id not in policy:
            raise ValueError(f"Missing policy: {case_id}")

        result = assess_security(
            action=row["predicted"],
            tool=row["tool"],
            target=row["target"],
            policy=policy[case_id],
        )

        assessed.append({
            **row,
            "security_assessment": result,
        })

    with (output / "assessed_predictions.csv").open(
        "w", newline=""
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=assessed[0].keys()
        )
        writer.writeheader()
        writer.writerows(assessed)

    print("\n=== CMU V2 SECURITY ANALYSIS ===")
    print("Total evaluations:", len(assessed))

    summary = {}

    for variant in ("baseline", "oversight"):
        subset = [
            r for r in assessed
            if r["variant"] == variant
        ]

        counts = Counter(
            r["security_assessment"]
            for r in subset
        )

        summary[variant] = {
            "total": len(subset),
            "security_assessments": dict(counts),
        }

        print(f"\n{variant.upper()}")
        for status, count in sorted(counts.items()):
            print(f"  {status}: {count}")

    (output / "security_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )

    print("\nSaved:", output)
    print("No model calls or real tools executed.")


if __name__ == "__main__":
    main()
