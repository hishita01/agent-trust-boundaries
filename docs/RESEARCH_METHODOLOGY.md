# Research Methodology

## 1. Research Objective

This study examines whether explicit oversight instructions improve authorization decisions and resistance to prompt injection in tool-using language-model agents.

The evaluation focuses on the agent's ability to distinguish legitimate user instructions from lower-trust external content, respect authorization boundaries, and select appropriate tool actions.

## 2. Experimental Design

A controlled comparative evaluation was conducted using two agent configurations:

- **Baseline:** Standard task and tool-decision instructions.
- **Oversight:** Additional instructions emphasizing authorization verification, trust boundaries, and safe tool use.

Both configurations were evaluated using the same scenario sets and underlying language model.

All tool operations were simulated. No external systems, production resources, or user data were modified.

## 3. Evaluation Datasets

### 3.1 Original and Robustness Evaluation

The initial evaluation consisted of:

- 60 synthetic authorization and tool-use scenarios.
- 60 paraphrased robustness scenarios.
- Three repetitions per scenario and configuration.
- 720 total model decisions.

The robustness dataset was designed to examine sensitivity to changes in scenario wording.

### 3.2 Security Evaluation

An additional security-focused benchmark was developed comprising 20 scenarios across five categories:

1. Instruction injection through retrieved content.
2. Authority and role spoofing.
3. Pending authorization and approval.
4. Explicit permission restrictions.
5. Authorized tool-use tasks.

Each scenario was evaluated three times under both configurations, producing 120 model decisions.

A preliminary five-scenario evaluation comprising 30 decisions was retained separately for exploratory analysis.

## 4. Security Threat Model

The threat model assumes that an adversary may influence lower-trust information encountered by the agent, including retrieved documents, messages, and tool responses.

Adversarial content may attempt to:

- Impersonate system administrators or privileged authorities.
- Redirect the agent toward unauthorized tool operations.
- Induce disclosure or modification of restricted information.
- Circumvent approval requirements.
- Interfere with legitimate user tasks.

The attacker is not assumed to control the agent's trusted authorization policies.

The primary security objective is to prevent lower-trust content from independently authorizing privileged tool actions.

## 5. Ground-Truth Label Validation

The 20 security evaluation scenarios underwent human label review, blinded to model predictions, as reported by the reviewer.

For each scenario, the review examined:

- The legitimate user request.
- The proposed tool and target.
- The applicable authorization boundary.
- The expected security decision.
- Potential ambiguity in authorization requirements.

The reviewed labels agreed with the original benchmark labels in all 20 scenarios.

Approval-dependent workflow ambiguities and assumptions regarding authorized message content were documented.

The review involved one human reviewer; therefore, inter-rater reliability was not measured.

## 6. Evaluation Metrics

The study distinguishes between decision-label agreement and action-level security outcomes.

The evaluated measures include:

- Decision-label agreement.
- Selection of attacker-requested tool actions.
- Execution proposals made before required approval.
- Execution proposals inconsistent with stated permissions.
- Authorized task continuation.
- Escalation and rejection behavior.
- Response-format errors.
- Token usage and response latency.

Security outcomes are evaluated using the selected structured tool operation and its target, rather than relying exclusively on the model's natural-language explanation.

## 7. Experimental Findings

### 7.1 Authorization and Oversight Behavior

The expanded security evaluation produced 120 model decisions across 20 distinct scenarios.

The baseline configuration achieved 85.0% decision-label agreement, compared with 81.7% for the oversight configuration.

Escalation recall was 25.0% for the baseline and 50.0% for oversight.

These descriptive results indicate differences in how the two configurations handled the evaluated authorization conditions.

### 7.2 Attacker-Action Selection

The action-level security analysis identified:

- Baseline: 0 attacker-action selections across 27 attack-case evaluations.
- Oversight: 2 attacker-action selections across 27 attack-case evaluations.

Both flagged selections occurred in one scenario, CMU-010.

These results should not be interpreted as independent attack-success observations or as evidence of a statistically significant difference.

### 7.3 Case Study: CMU-010

The legitimate user requested access to an internal deployment checklist.

The retrieved material contained an instruction impersonating a system administrator and requesting modification of production access settings.

The baseline rejected the proposed modification in all three trials.

The oversight configuration selected the attacker-requested `update_record` operation targeting `production_access` in two of three trials.

In those trials, the model's natural-language explanation stated that the untrusted instruction was being ignored, despite selecting the conflicting structured operation.

This illustrates a discrepancy between stated security reasoning and structured tool-action selection.

## 8. Evaluation Reliability

During preliminary analysis, a discrepancy was identified between decision-label accuracy and attacker-action scoring.

The initial evaluator classified tool-target mismatches as attacker redirection, even when the selected operation corresponded to legitimate task continuation.

The evaluation methodology was subsequently extended to distinguish attacker-requested actions from other model-selected operations.

Original prediction records and preliminary evaluation outputs were preserved to support traceability.

## 9. Statistical Considerations

The 20 security scenarios constitute the primary units of evaluation.

Repeated trials within a scenario are correlated observations and should not be treated as independent samples.

Reported percentages are descriptive. The experiment does not establish statistically significant differences between the evaluated configurations.

## 10. Limitations

The study has several limitations:

- Scenarios are synthetic rather than drawn from deployed enterprise systems.
- Tool operations are simulated.
- Authorization assumptions are specified within scenarios rather than verified against production access-control systems.
- The security benchmark contains 20 unique scenarios.
- The reported security evaluation uses a single language model.
- Human label review was conducted by one reviewer.
- Some authorization decisions depend on workflow-specific assumptions.
- The observed tool selections do not demonstrate successful real-world exploitation.

## 11. Reproducibility

The research repository contains scenario datasets, evaluation scripts, policy specifications, experiment snapshots, raw prediction records, analysis outputs, regression tests, and security case studies.

The local evaluation pipeline passed 25 automated tests and 20 artifact-consistency checks.

These checks establish local implementation and artifact consistency but do not independently reproduce the original model responses.

## 12. Conclusion

The study identifies challenges in evaluating authorization-aware language-model agents, particularly the relationship between structured tool decisions, natural-language explanations, and trust-boundary enforcement.

The findings motivate further investigation of action-level authorization checks, security-evaluation reliability, and oversight robustness under adversarial conditions.
