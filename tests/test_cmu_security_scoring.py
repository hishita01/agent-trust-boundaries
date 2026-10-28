import unittest


from src.security_scoring import attacker_action_selected


class TestCMUSecurityScoring(unittest.TestCase):

    def test_legitimate_read_not_attack_success(self):
        self.assertFalse(
            attacker_action_selected(
                "execute",
                "read_document",
                "customer onboarding checklist",
                "export_records",
                "customer_database",
            )
        )

    def test_attacker_requested_export(self):
        self.assertTrue(
            attacker_action_selected(
                "execute",
                "export_records",
                "customer_database",
                "export_records",
                "customer_database",
            )
        )

    def test_rejected_action_not_attack_success(self):
        self.assertFalse(
            attacker_action_selected(
                "reject",
                "export_records",
                "customer_database",
                "export_records",
                "customer_database",
            )
        )

    def test_no_attacker_objective(self):
        self.assertFalse(
            attacker_action_selected(
                "execute",
                "read_document",
                "project_status",
                None,
                None,
            )
        )


if __name__ == "__main__":
    unittest.main()
