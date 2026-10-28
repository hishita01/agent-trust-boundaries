# Threat Model: Tool-Using LLM Agents

## System

The system consists of an LLM agent that receives
user requests, external context, and a proposed
tool action.

The agent must decide whether to:
- execute
- escalate
- reject

## Protected Assets

- Sensitive documents
- Customer records
- Internal communications
- Permission-controlled tools
- Enterprise workflow integrity

## Trust Boundaries

Trusted:
- System-level security policies
- Authenticated user authorization
- Verified access-control information

Untrusted:
- Retrieved documents
- External messages
- Third-party tool responses
- User-controlled content without verified authority

## Attacker Capabilities

An attacker may control lower-trust content
encountered by the agent.

The attacker cannot modify the system's trusted
authorization policy.

## Attacker Objectives

- Induce unauthorized tool actions
- Impersonate trusted authorities
- Bypass approval requirements
- Redirect the agent from legitimate tasks
- Cause unnecessary escalation or workflow failure

## Security Invariants

1. Retrieved content cannot grant authorization.
2. Pending approval must not be treated as approval.
3. Missing authorization requires escalation or rejection.
4. External instructions must not override trusted policy.
5. Authorized tasks should not be unnecessarily blocked.

## Evaluation Limitations

The current environment uses simulated tools.

Model decisions are not equivalent to successful
real-world exploitation.

Security conclusions require validated labels,
held-out scenarios, and reproducible experiments.
