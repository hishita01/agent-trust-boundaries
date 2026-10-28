# Enterprise AI Governance, Authorization, and Risk Review

## 1. Executive Summary

This review examines enterprise governance controls for
tool-using language-model agents in the AI Agent Oversight
& Trust Boundary Evaluation research project.

The objective is to determine whether agent-selected tool
operations can be evaluated against enterprise identity,
permission, approval, and data-handling requirements
before simulated execution.

A governance evaluation prototype was implemented and
integrated with the project's independent authorization
gate and protected simulated executor.

The resulting architecture demonstrates defense in depth:
both governance eligibility and exact tool-target
authorization must pass before simulated execution.

The implementation is a research prototype, not a
production enterprise authorization system.

## 2. Enterprise Governance Requirements

The proposed governance framework includes:

- Verified user identity
- Active authenticated sessions
- Role information
- Explicit permission checks
- Approval verification
- Approval scope matching
- Approval expiration checks
- Separation of requester and approver
- Data classification
- Restrictions on external disclosure
- Default-deny authorization
- Decision auditability

The framework distinguishes between execution,
escalation, and rejection.

## 3. Governance Policy Specification

Policy file:

data/enterprise_governance_policy.json

The policy defines least-privilege principles, identity
requirements, approval conditions, data classifications,
tool risk levels, and audit requirements.

The classifications and control rules are illustrative
research assumptions.

The JSON policy is a governance specification. The
prototype evaluator implements a subset of its rules;
it does not dynamically load or fully enforce the
entire policy document.

## 4. Governance Evaluation Engine

Implementation:

src/enterprise_governance.py

The evaluator returns one of three decisions:

### Execute

The supplied trusted context satisfies the implemented
identity, permission, classification, and approval rules.

### Escalate

Required authorization information is unavailable,
approval is pending or expired, or a required identity
or classification fact cannot be verified.

### Reject

The operation is prohibited, permission is explicitly
denied, the requested tool is unsupported, an approval
scope does not match, or external disclosure violates
the implemented classification rule.

These decisions describe simulated policy behavior
and do not initiate enterprise approval workflows.

## 5. Integration with Protected Execution

Implementation:

src/enterprise_pipeline.py

The integrated processing sequence is:

1. Parse the model-generated structured decision.
2. Evaluate enterprise governance eligibility.
3. Check exact tool-target authorization using the
   independent authorization gate.
4. Execute only permitted simulated tool operations.
5. Record the resulting simulated decision event.

A governance approval cannot independently override
a denial from the authorization gate.

Model explanations are not accepted as permission or
approval evidence.

## 6. Security Scenario: CMU-010

The underlying research identified a scenario in which
untrusted retrieved content attempted to redirect an
agent from reading a deployment checklist to changing
production access settings.

In two recorded oversight trials, the model selected
the attacker-requested structured tool action despite
explaining that the malicious instruction was ignored.

The Apple engineering protected replay blocked both
attacker-selected actions under a trusted authorization
fixture permitting only the legitimate document read.

The governance integration provides a further policy
evaluation layer for identity, permission, approval,
and data restrictions.

The historical replay and the governance integration
tests are separate evaluations. No new live-model
governance experiment was conducted.

## 7. Verification

The combined local automated test suite passed
57 tests.

Governance-specific tests cover:

- Valid approved operations
- Missing identity information
- Explicit permission denial
- Unknown permissions
- Pending approval
- Requester self-approval
- Expired approvals
- Approval scope mismatch
- Restricted external disclosure
- Authorized internal document reads

Integration tests additionally verify:

- Authorized reads reach the protected simulator
- CMU-010-style unauthorized actions do not execute
- Pending approval prevents execution
- Denied permissions prevent execution
- Governance approval cannot override the tool gate
- Missing trusted grants prevent execution

These tests establish behavior under their specific
fixtures, not comprehensive enterprise security.

## 8. Enterprise Risk Assessment

### Risk 1: Forged identity or permissions

The prototype trusts caller-supplied identity and
permission information.

Production systems must obtain and verify these facts
through authoritative identity and access-management
services.

### Risk 2: Unauthorized approval

The prototype checks approval status, approver identity
difference, tool, target, and expiration.

It does not verify that the approver has authority to
approve the operation, or that approval evidence was
issued by a trusted service.

### Risk 3: Policy specification drift

The JSON policy is not dynamically enforced by the
current governance evaluator.

Changes to the policy document do not automatically
change enforcement behavior.

### Risk 4: Sensitive-data disclosure

The prototype checks a caller-supplied classification
and external-destination flag.

It does not independently classify data, validate
recipient domains, inspect actual payloads, or provide
data-loss-prevention integration.

### Risk 5: Incomplete authorization scope

Tool and target matching is necessary but may be
insufficient for production operations.

Action parameters, record scope, transaction amount,
recipient identity, and environmental context may
also require policy enforcement.

### Risk 6: Audit integrity

The prototype records simulated decision events.

It does not implement persistent, tamper-evident audit
storage, retention policies, or enterprise monitoring.

### Risk 7: Approval reuse and concurrency

The prototype does not implement approval revocation,
single-use grants, replay prevention, or transaction-
atomic authorization checks.

These controls are important for enterprise execution
systems.

## 9. Recommended Production Controls

Before a production deployment, implement:

1. Authoritative authentication and identity validation.
2. Permission checks against trusted access-control
   systems.
3. Signed or otherwise verifiable scoped approvals.
4. Approver authority and separation-of-duties checks.
5. Approval expiration and revocation enforcement.
6. Parameter- and resource-level authorization.
7. Trusted data-classification and destination checks.
8. Tamper-evident audit logging and monitoring.
9. Replay protection and concurrency safeguards.
10. Independent red-team and security validation.

## 10. Research Limitations

The evaluation uses synthetic scenarios and simulated
tool operations.

The governance layer has not been evaluated against
real enterprise identity providers, approval services,
external tools, or production workloads.

The local tests establish deterministic behavior of
the prototype under controlled assumptions.

They do not establish statistical effectiveness against
real-world attacks or production deployment readiness.

## 11. Conclusion

The enterprise governance contribution extends the
research prototype beyond prompt-level oversight and
basic tool-target authorization.

It demonstrates a layered architecture in which
enterprise governance eligibility and an independent
authorization gate must both permit an operation
before simulated execution.

The principal finding is architectural: language-model
tool selections should not be treated as authorization,
and enterprise control decisions must be enforced
outside the language model.

The prototype supports this design principle while
identifying substantial controls needed before
deployment in an enterprise environment.
