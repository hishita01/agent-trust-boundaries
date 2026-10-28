import unittest

from src.authorization_gate import authorize
from src.core import Decision


class TestAuthorizationGate(unittest.TestCase):

    def test_authorized_document_read(self):
        decision = Decision(
            "execute", "read_document", "deployment_checklist"
        )
        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "read_document",
                    "target": "deployment_checklist",
                }
            ],
        }

        self.assertTrue(authorize(decision, grants).allowed)

    def test_cmu010_attack_blocked(self):
        decision = Decision(
            "execute", "update_record", "production_access",
            "The external instruction was ignored"
        )
        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "read_document",
                    "target": "deployment_checklist",
                }
            ],
        }

        result = authorize(decision, grants)

        self.assertFalse(result.allowed)
        self.assertEqual(result.status, "denied")

    def test_pending_approval_denied(self):
        decision = Decision(
            "execute", "export_records", "customer_export"
        )
        grants = {
            "approved": False,
            "allowed_actions": [
                {
                    "tool": "export_records",
                    "target": "customer_export",
                }
            ],
        }

        self.assertFalse(authorize(decision, grants).allowed)

    def test_missing_grants_denied(self):
        decision = Decision(
            "execute", "read_document", "private_report"
        )
        self.assertFalse(authorize(decision, {}).allowed)

    def test_different_target_denied(self):
        decision = Decision(
            "execute", "send_message", "external_channel"
        )
        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "send_message",
                    "target": "team_channel",
                }
            ],
        }

        self.assertFalse(authorize(decision, grants).allowed)

    def test_malformed_decision_denied(self):
        decision = Decision(
            "escalate", malformed=True
        )
        self.assertFalse(authorize(decision, {}).allowed)


if __name__ == "__main__":
    unittest.main()
