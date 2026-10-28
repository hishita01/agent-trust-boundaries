"""Enterprise AI governance evaluator.

Simulation only. Caller-provided context is assumed trusted;
no real identity provider or approval system is connected.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class GovernanceResult:
    decision: str
    reason: str


def evaluate_governance(
    *,
    tool,
    target,
    identity,
    permission,
    approval,
    classification,
    destination_external=False,
    now=None,
):
    """Return execute, escalate, or reject.

    All arguments must originate from trusted infrastructure,
    not the language model or retrieved external content.
    """
    if tool not in {
        "read_document",
        "update_record",
        "send_message",
        "export_records",
    }:
        return GovernanceResult("reject", "Unsupported tool")

    if not isinstance(target, str) or not target:
        return GovernanceResult("reject", "Invalid target")

    if not isinstance(identity, dict):
        return GovernanceResult("escalate", "Identity verification unavailable")

    if (
        identity.get("verified") is not True
        or identity.get("session_active") is not True
        or not identity.get("role")
        or not identity.get("user_id")
    ):
        return GovernanceResult("escalate", "Identity not fully verified")

    if permission is False:
        return GovernanceResult("reject", "Permission explicitly denied")

    if permission is not True:
        return GovernanceResult("escalate", "Permission requires verification")

    if classification not in {
        "public", "internal", "confidential", "restricted"
    }:
        return GovernanceResult("escalate", "Classification unavailable")

    if destination_external and classification != "public":
        return GovernanceResult("reject", "External disclosure prohibited")

    # Additional approval is required for sensitive information
    # and high-risk operations.
    approval_required = (
        classification in {"confidential", "restricted"}
        or tool in {"update_record", "export_records"}
    )

    if approval_required:
        if not isinstance(approval, dict):
            return GovernanceResult("escalate", "Approval missing")

        if approval.get("status") == "denied":
            return GovernanceResult("reject", "Approval denied")

        if approval.get("status") != "approved":
            return GovernanceResult("escalate", "Approval pending")

        if approval.get("approver_id") == identity["user_id"]:
            return GovernanceResult("reject", "Self-approval prohibited")

        if (
            approval.get("tool") != tool
            or approval.get("target") != target
        ):
            return GovernanceResult("reject", "Approval scope mismatch")

        expires_at = approval.get("expires_at")
        if not isinstance(expires_at, str):
            return GovernanceResult("escalate", "Approval expiry unavailable")

        try:
            expiry = datetime.fromisoformat(
                expires_at.replace("Z", "+00:00")
            )
            if expiry.tzinfo is None:
                raise ValueError("Timezone required")
        except ValueError:
            return GovernanceResult("escalate", "Invalid approval expiry")

        if now is None:
            now = datetime.now(timezone.utc)

        if now >= expiry:
            return GovernanceResult("escalate", "Approval expired")

    return GovernanceResult("execute", "Governance checks passed")
