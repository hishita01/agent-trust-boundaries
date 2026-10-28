"""Combined governance and protected execution pipeline.

Research simulation only. No real external tool operations.
"""

from .core import parse_decision
from .enterprise_governance import evaluate_governance
from .protected_executor import ProtectedExecutor


def process_enterprise_action(
    raw_decision,
    *,
    trusted_grants,
    identity,
    permission,
    approval,
    classification,
    destination_external=False,
    now=None,
):
    """Require both governance and tool authorization.

    Trusted inputs must originate outside the language model.
    """
    decision = parse_decision(raw_decision)
    executor = ProtectedExecutor()

    if decision.action != "execute":
        reason = (
            "Malformed model decision"
            if decision.malformed
            else "Model did not request execution"
        )
        return {
            "governance_decision": "reject" if decision.malformed
                                   else decision.action,
            "event": {
                "allowed": False,
                "executed": False,
                "reason": reason,
            },
            "state": executor.state,
            "audit_log": [],
        }

    governance = evaluate_governance(
        tool=decision.tool,
        target=decision.target,
        identity=identity,
        permission=permission,
        approval=approval,
        classification=classification,
        destination_external=destination_external,
        now=now,
    )

    if governance.decision != "execute":
        event = {
            "allowed": False,
            "executed": False,
            "reason": governance.reason,
        }
        executor.log.append({
            "stage": "governance",
            "decision": governance.decision,
            **event,
        })
        return {
            "governance_decision": governance.decision,
            "event": event,
            "state": executor.state,
            "audit_log": executor.log,
        }

    # Governance approval does not create or expand
    # the independently supplied authorization grants.
    event = executor.apply(decision, trusted_grants)

    return {
        "governance_decision": governance.decision,
        "event": event,
        "state": executor.state,
        "audit_log": executor.log,
    }
