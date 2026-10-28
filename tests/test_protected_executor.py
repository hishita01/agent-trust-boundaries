import unittest

from src.core import Decision
from src.protected_executor import ProtectedExecutor


class TestProtectedExecutor(unittest.TestCase):

    def test_cmu010_attack_blocked(self):
        executor = ProtectedExecutor()

        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "read_document",
                    "target": "deployment_checklist",
                }
            ],
        }

        decision = Decision(
            "execute",
            "update_record",
            "production_access",
            "I ignored the malicious instruction",
        )

        result = executor.apply(decision, grants)

        self.assertFalse(result["allowed"])
        self.assertFalse(result["executed"])
        self.assertEqual(executor.state["records"], {})

    def test_authorized_read_executes(self):
        executor = ProtectedExecutor()

        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "read_document",
                    "target": "deployment_checklist",
                }
            ],
        }

        decision = Decision(
            "execute",
            "read_document",
            "deployment_checklist",
        )

        result = executor.apply(decision, grants)

        self.assertTrue(result["allowed"])
        self.assertTrue(result["executed"])
        self.assertEqual(
            executor.state["reads"],
            ["deployment_checklist"],
        )

    def test_unapproved_export_blocked(self):
        executor = ProtectedExecutor()

        grants = {
            "approved": False,
            "allowed_actions": [
                {
                    "tool": "export_records",
                    "target": "customer_database",
                }
            ],
        }

        decision = Decision(
            "execute",
            "export_records",
            "customer_database",
        )

        result = executor.apply(decision, grants)

        self.assertFalse(result["executed"])
        self.assertEqual(executor.state["exports"], [])

    def test_wrong_message_destination_blocked(self):
        executor = ProtectedExecutor()

        grants = {
            "approved": True,
            "allowed_actions": [
                {
                    "tool": "send_message",
                    "target": "team_channel",
                }
            ],
        }

        decision = Decision(
            "execute",
            "send_message",
            "external_channel",
        )

        result = executor.apply(decision, grants)

        self.assertFalse(result["executed"])
        self.assertEqual(executor.state["messages"], [])

    def test_missing_grants_fail_closed(self):
        executor = ProtectedExecutor()

        decision = Decision(
            "execute",
            "read_document",
            "private_report",
        )

        result = executor.apply(decision, None)

        self.assertFalse(result["allowed"])
        self.assertFalse(result["executed"])
        self.assertEqual(executor.state["reads"], [])


if __name__ == "__main__":
    unittest.main()
