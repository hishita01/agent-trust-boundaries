# Authorization Enforcement Ablation

## Objective

Evaluate how independent authorization enforcement changes
the handling of previously recorded language-model tool
decisions in the security benchmark.

## Experimental Design

The analysis replays 120 recorded model decisions from
20 security scenarios, with three trials per scenario
and two model configurations.

Three execution policies are compared:

1. Model-only: retain the raw execution proposal.
2. Authorization gate: enforce a trusted exact-match
   tool-target allowlist.
3. Enterprise governance plus authorization gate:
   enforce simulated identity, permission, approval,
   and classification checks before tool authorization.

The model-only configuration represents proposed actions,
not confirmed tool execution.

No new model calls were made.

## Authorization Assumptions

Only scenarios marked explicitly authorized receive
synthetic tool-target grants.

Pending-approval, permission-denied, and attacker-action
scenarios receive no executable grants.

The identity and governance inputs are controlled
research fixtures, not independently verified
enterprise credentials or approvals.

These assumptions make the experiment conservative
and can block legitimate actions when authorization
evidence is unavailable.

## Results

| Measure | Baseline | Oversight |
|---|---:|---:|
| Recorded decisions | 60 | 60 |
| Raw execution proposals | 9 | 14 |
| Attacker-action selections | 0 | 2 |
| Gate-permitted simulated executions | 9 | 9 |
| Governance + gate permitted executions | 9 | 9 |
| Attacker actions permitted by either protected path | 0 | 0 |

Both identified attacker-action selections originated
from scenario CMU-010.

Both were denied by each protected configuration.

Among the five oversight execution proposals denied by
the protected configurations, two matched the explicit
attacker objective and three were other execution
proposals requiring review.

The replay does not establish that all denied proposals
were real-world security violations.

## Interpretation

The recorded model decisions demonstrate that a
natural-language explanation of safe behavior does not
guarantee a safe structured tool selection.

Under trusted policy fixtures, an independent execution
gate prevented the two observed attacker-action
selections from reaching simulated execution.

The enterprise-governance configuration permitted the
same number of actions as the authorization gate alone.

Consequently, this experiment does not demonstrate
incremental enforcement effectiveness from enterprise
governance beyond exact-match authorization.

## Limitations

- This is an offline counterfactual replay.
- The security dataset contains 20 unique scenarios.
- Repeated trials are not independent scenarios.
- All tool operations are simulated.
- Authorization and governance facts are supplied
  through research fixtures.
- Prompt-injection scenarios lack independently verified
  grants for legitimate task continuation.
- The experiment does not measure production security,
  real identity validation, or approval-service behavior.
- The policy was designed and evaluated with knowledge
  of the benchmark structure.
- No statistical significance claim is made.

## Reproducibility

Input:
results/cmu-v2-live/live_predictions.csv

Frozen dataset:
results/cmu-v2-live/dataset_snapshot.jsonl

Frozen policy:
results/cmu-v2-live/policy_snapshot.json

Implementation:
scripts/authorization_ablation.py

Outputs:
results/authorization-ablation/decisions.csv
results/authorization-ablation/summary.json

Run:
python -m scripts.authorization_ablation
