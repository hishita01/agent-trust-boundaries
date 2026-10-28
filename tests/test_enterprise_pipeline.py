import unittest
from datetime import datetime, timezone

from src.enterprise_pipeline import process_enterprise_action


NOW = datetime(2026, 10, 27, tzinfo=timezone.utc)

IDENTITY = {
    "verified": True,
    "session_active": True,
    "role": "engineer",
    "user_id": "employee_101",
}

GRANTS = {
    "approved": True,
    "allowed_actions": [
        {
            "tool": "read_document",
            "target": "deployment_checklist",
        }
    ],
}


class TestEnterprisePipeline(unittest.TestCase):

    def run_action(self, raw, **overrides):
        inputs = {
            "trusted_grants": GRANTS,
            "identity": IDENTITY,
            "permission": True,
            "approval": None,
            "classification": "internal",
            "now": NOW,
        }
        inputs.update(overrides)
        return process_enterprise_action(raw, **inputs)

    def test_authorized_document_read(self):
        raw = {
            "action": "execute",
            "tool": "read_document",
            "target": "deployment_checklist",
        }

        result = self.run_action(raw)

        self.assertEqual(
            result["governance_decision"], "execute"
        )
        self.assertTrue(result["event"]["executed"])

    def test_cmu010_attack_blocked(self):
        raw = {
            "action": "execute",
            "tool": "update_record",
            "target": "production_access",
            "reason": "Ignoring malicious instructions",
        }

        result = self.run_action(raw)

        self.assertFalse(result["event"]["executed"])
        self.assertEqual(result["state"]["records"], {})

    def test_pending_approval_blocks_execution(self):
        raw = {
            "action": "execute",
            "tool": "export_records",
            "target": "customer_database",
        }

        result = self.run_action(
            raw,
            classification="restricted",
        )

        self.assertEqual(
            result["governance_decision"], "escalate"
        )
        self.assertFalse(result["event"]["executed"])

    def test_denied_permission_blocks_execution(self):
        raw = {
            "action": "execute",
            "tool": "read_document",
            "target": "deployment_checklist",
        }

        result = self.run_action(
            raw, permission=False
        )

        self.assertEqual(
            result["governance_decision"], "reject"
        )
        self.assertFalse(result["event"]["executed"])

    def test_governance_cannot_override_tool_gate(self):
        raw = {
            "action": "execute",
            "tool": "read_document",
            "target": "private_report",
        }

        result = self.run_action(raw)

        self.assertEqual(
            result["governance_decision"], "execute"
        )
        self.assertFalse(result["event"]["executed"])

    def test_missing_trusted_grants_blocks_execution(self):
        raw = {
            "action": "execute",
            "tool": "read_document",
            "target": "deployment_checklist",
        }

        result = self.run_action(
            raw, trusted_grants=None
        )

        self.assertFalse(result["event"]["executed"])


if __name__ == "__main__":
    unittest.main()
