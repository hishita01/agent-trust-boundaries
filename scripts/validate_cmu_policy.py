import json
from collections import Counter
from pathlib import Path

dataset_path = Path("data/cmu_security_holdout_v2.jsonl")
policy_path = Path("data/cmu_security_policy_v2.json")

cases = [
    json.loads(line)
    for line in dataset_path.read_text().splitlines()
    if line.strip()
]

policy = json.loads(policy_path.read_text())

expected_status = {
    "instruction_in_data": "attacker_action_unauthorized",
    "role_spoof": "attacker_action_unauthorized",
    "approval_pending": "approval_pending",
    "missing_permission": "permission_denied",
    "clean": "authorized",
}

errors = []
ids = [case["id"] for case in cases]

if len(ids) != len(set(ids)):
    errors.append("Duplicate scenario IDs found")

if set(ids) != set(policy):
    errors.append("Dataset and policy IDs do not match")

for case in cases:
    case_id = case["id"]
    p = policy.get(case_id)

    if p is None:
        continue

    category = case["category"]
    status = p["authorization_status"]

    if status != expected_status.get(category):
        errors.append(f"{case_id}: incorrect authorization status")

    is_attack = category in {
        "instruction_in_data",
        "role_spoof",
    }

    if is_attack:
        if p["attacker_tool"] != case["tool"]:
            errors.append(f"{case_id}: attacker tool mismatch")

        if p["attacker_target"] != case["target"]:
            errors.append(f"{case_id}: attacker target mismatch")

    else:
        if p["attacker_tool"] is not None:
            errors.append(f"{case_id}: unexpected attacker tool")

        if p["attacker_target"] is not None:
            errors.append(f"{case_id}: unexpected attacker target")

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("CMU SECURITY POLICY VALIDATION PASSED")
print("Total scenarios:", len(cases))
print("Policy entries:", len(policy))

print("\nAuthorization categories:")
counts = Counter(
    p["authorization_status"]
    for p in policy.values()
)

for status, count in sorted(counts.items()):
    print(f"{status}: {count}")

print("\nAll structural checks passed.")
print("Human review of authorization remains required.")
