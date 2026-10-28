import unittest
from datetime import datetime, timezone

from src.enterprise_governance import evaluate_governance


IDENTITY = {
    "verified": True,
    "session_active": True,
    "role": "engineer",
    "user_id": "employee_101",
}

APPROVAL = {
    "status": "approved",
    "approver_id": "manager_202",
    "tool": "update_record",
    "target": "production_access",
    "expires_at": "2027-01-01T00:00:00+00:00",
}

NOW = datetime(2026, 10, 27, tzinfo=timezone.utc)


class TestEnterpriseGovernance(unittest.TestCase):

    def evaluate(self, **overrides):
        args = {
            "tool": "update_record",
            "target": "production_access",
            "identity": IDENTITY,
            "permission": True,
            "approval": APPROVAL,
            "classification": "restricted",
            "now": NOW,
        }
        args.update(overrides)
        return evaluate_governance(**args)

    def test_valid_approved_operation(self):
        self.assertEqual(self.evaluate().decision, "execute")

    def test_missing_identity_escalates(self):
        self.assertEqual(
            self.evaluate(identity=None).decision, "escalate"
        )

    def test_permission_denied_rejects(self):
        self.assertEqual(
            self.evaluate(permission=False).decision, "reject"
        )

    def test_permission_unknown_escalates(self):
        self.assertEqual(
            self.evaluate(permission=None).decision, "escalate"
        )

    def test_pending_approval_escalates(self):
        self.assertEqual(
            self.evaluate(
                approval={**APPROVAL, "status": "pending"}
            ).decision,
            "escalate",
        )

    def test_self_approval_rejected(self):
        self.assertEqual(
            self.evaluate(
                approval={
                    **APPROVAL,
                    "approver_id": "employee_101",
                }
            ).decision,
            "reject",
        )

    def test_expired_approval_escalates(self):
        self.assertEqual(
            self.evaluate(
                approval={
                    **APPROVAL,
                    "expires_at": "2026-01-01T00:00:00Z",
                }
            ).decision,
            "escalate",
        )

    def test_wrong_approval_scope_rejected(self):
        self.assertEqual(
            self.evaluate(
                approval={
                    **APPROVAL,
                    "target": "different_record",
                }
            ).decision,
            "reject",
        )

    def test_restricted_external_disclosure_rejected(self):
        self.assertEqual(
            self.evaluate(destination_external=True).decision,
            "reject",
        )

    def test_authorized_internal_read(self):
        self.assertEqual(
            self.evaluate(
                tool="read_document",
                target="engineering_handbook",
                classification="internal",
                approval=None,
            ).decision,
            "execute",
        )


if __name__ == "__main__":
    unittest.main()
