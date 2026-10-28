"""Protected model-decision pipeline. Simulation only."""

from .core import parse_decision
from .protected_executor import ProtectedExecutor


def process_model_output(raw_decision, trusted_grants):
    """Parse, authorize, then simulate an agent tool decision.

    trusted_grants must come from a trusted caller,
    not retrieved content or model-generated fields.
    """
    decision = parse_decision(raw_decision)
    executor = ProtectedExecutor()
    event = executor.apply(decision, trusted_grants)

    return {
        "decision": decision,
        "event": event,
        "state": executor.state,
        "audit_log": executor.log,
    }
