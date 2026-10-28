"""Independent, fail-closed authorization gate.

This module never executes real external tools.
"""

from dataclasses import dataclass

from .core import TOOLS, Decision


@dataclass(frozen=True)
class GateResult:
    allowed: bool
    status: str
    reason: str


def authorize(decision: Decision, grants: dict) -> GateResult:
    """Authorize a model-selected action using trusted grants.

    grants must be supplied by a trusted policy source,
    never from model output or retrieved external content.

    Format:
    {
        "approved": True,
        "allowed_actions": [
            {"tool": "read_document", "target": "document_id"}
        ]
    }
    """
    if decision.malformed:
        return GateResult(False, "denied", "Malformed model decision")

    if decision.action != "execute":
        return GateResult(False, "not_executed", "No execution requested")

    if decision.tool not in TOOLS:
        return GateResult(False, "denied", "Unsupported tool")

    if not isinstance(decision.target, str) or not decision.target:
        return GateResult(False, "denied", "Invalid target")

    if not isinstance(grants, dict):
        return GateResult(False, "denied", "Missing trusted grants")

    if grants.get("approved") is not True:
        return GateResult(False, "denied", "Approval not verified")

    allowed_actions = grants.get("allowed_actions")

    if not isinstance(allowed_actions, list):
        return GateResult(False, "denied", "Missing action allowlist")

    for entry in allowed_actions:
        if not isinstance(entry, dict):
            continue

        if (
            entry.get("tool") == decision.tool
            and entry.get("target") == decision.target
        ):
            return GateResult(True, "allowed", "Trusted authorization matched")

    return GateResult(False, "denied", "Tool or target not authorized")
