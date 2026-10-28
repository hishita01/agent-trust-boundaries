"""Policy-gated simulated tool executor.

No real external tools or network operations.
"""

from .authorization_gate import authorize


class ProtectedExecutor:
    def __init__(self):
        self.state = {
            "records": {},
            "messages": [],
            "reads": [],
            "exports": [],
        }
        self.log = []

    def apply(self, decision, trusted_grants):
        """Authorize before executing any simulated operation."""

        result = authorize(decision, trusted_grants)

        event = {
            "requested_action": decision.action,
            "tool": decision.tool,
            "target": decision.target,
            "allowed": result.allowed,
            "status": result.status,
            "reason": result.reason,
        }

        if not result.allowed:
            event["executed"] = False
            self.log.append(event)
            return event

        # Only supported, authorized actions reach this point.
        if decision.tool == "read_document":
            self.state["reads"].append(decision.target)

        elif decision.tool == "update_record":
            self.state["records"][decision.target] = (
                "simulated_updated"
            )

        elif decision.tool == "send_message":
            self.state["messages"].append({
                "to": decision.target,
                "body": "simulated_only",
            })

        elif decision.tool == "export_records":
            self.state["exports"].append(decision.target)

        else:
            raise RuntimeError(
                "Unsupported tool passed authorization gate"
            )

        event["executed"] = True
        self.log.append(event)
        return event
