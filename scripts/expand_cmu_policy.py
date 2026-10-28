import json
from pathlib import Path

dataset = Path("data/cmu_security_holdout_v2.jsonl")
original_policy = Path("data/cmu_security_policy.json")
output = Path("data/cmu_security_policy_v2.json")

cases = [
    json.loads(line)
    for line in dataset.read_text().splitlines()
    if line.strip()
]

policy = json.loads(original_policy.read_text())

for case in cases:
    case_id = case["id"]

    if case_id in policy:
        continue

    category = case["category"]

    if category in {
        "instruction_in_data",
        "role_spoof",
    }:
        authorization_status = "attacker_action_unauthorized"
        attacker_tool = case["tool"]
        attacker_target = case["target"]

    elif category == "approval_pending":
        authorization_status = "approval_pending"
        attacker_tool = None
        attacker_target = None

    elif category == "missing_permission":
        authorization_status = "permission_denied"
        attacker_tool = None
        attacker_target = None

    elif category == "clean":
        authorization_status = "authorized"
        attacker_tool = None
        attacker_target = None

    else:
        raise ValueError(
            f"Unexpected category: {category}"
        )

    policy[case_id] = {
        "legitimate_task": case["user_request"],
        "attacker_objective": (
            f"Induce execution of "
            f"{attacker_tool} on {attacker_target}"
            if attacker_tool else None
        ),
        "attacker_tool": attacker_tool,
        "attacker_target": attacker_target,
        "authorization_status": authorization_status,
    }

assert len(policy) == 20
assert set(policy) == {case["id"] for case in cases}

output.write_text(
    json.dumps(policy, indent=2) + "\n"
)

print("CMU POLICY V2 CREATED")
print("Scenarios:", len(cases))
print("Policy entries:", len(policy))
print("Saved:", output)
print("Security rules remain provisional.")
