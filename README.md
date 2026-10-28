# AI Agent Oversight and Trust Boundary Evaluation

**An empirical study of prompt-injection resistance, authorization decisions, and trust-boundary enforcement in tool-using language-model agents.**

## Research Question

Do explicit oversight instructions improve authorization decisions and resistance to prompt injection in tool-using AI agents? Can independent authorization enforcement mitigate unsafe tool-action selections?

## Experimental Setup

- **Model:** GPT-5.4-mini
- **Original evaluation:** 60 synthetic scenarios
- **Robustness evaluation:** 60 paraphrased scenarios
- **Adversarial security evaluation:** 20 scenarios
- **Configurations:** Baseline and oversight
- **Repetitions:** 3 per configuration
- **Total primary live-model decisions:** 840
- **Tool execution:** Simulated; no external services accessed

## Key Findings

| Metric | Baseline | Oversight |
|---|---:|---:|
| Security decision-label agreement | 85.0% | 81.7% |
| Attacker-action selections | 0/27 | 2/27 |
| Escalation recall | 25.0% | 50.0% |
| Simulated executions permitted by authorization gate | 9 | 9 |

The security evaluation identified a case where the model selected an unauthorized tool action despite explaining that it was ignoring malicious instructions.

An offline enforcement replay demonstrated that an independent authorization gate blocked both observed attacker-action selections under defined policy assumptions.

The results are descriptive and do not establish general model vulnerability rates or statistical significance.

## Research Components

- **Experimental Evaluation:** Baseline, oversight, and robustness testing.
- **Adversarial Security Analysis:** Prompt-injection scenarios, threat modeling, and corrected security scoring.
- **Authorization Enforcement:** Independent tool authorization and protected simulated execution.
- **Enterprise AI Governance:** Permission checks, approval requirements, and risk assessment.
- **Reproducibility:** Recorded predictions, datasets, analysis scripts, and 57 automated tests.

## Reproducing the Results

See [PROJECT_START_HERE.md](PROJECT_START_HERE.md) for setup instructions and the evaluation workflow.

Run the automated tests:

```bash
python -m unittest discover -s tests -q
```

Verify research artifacts:

```bash
python -m scripts.final_reproducibility_check
```

Reproduce the offline authorization analysis:

```bash
python -m scripts.authorization_ablation
```

## Research Limitations

The study uses synthetic scenarios, simulated tool operations, and a single model for the expanded security evaluation. Security labels underwent single-reviewer human validation. The enforcement prototypes use predefined authorization fixtures rather than production identity or approval systems.

Findings require broader independent evaluation before conclusions about real-world security effectiveness can be drawn.

## Documentation

- [Research Methodology](docs/RESEARCH_METHODOLOGY.md)
- [Research Findings](docs/RESEARCH_FINDINGS.md)
- [Threat Model](docs/THREAT_MODEL.md)
- [Authorization Ablation](docs/AUTHORIZATION_ABLATION.md)
- [Agent Architecture Review](docs/APPLE_ENGINEERING_ARCHITECTURE_REVIEW.md)
- [Enterprise Governance Review](docs/ENTERPRISE_GOVERNANCE_REVIEW.md)
- [Research Contributions](CONTRIBUTORS.md)

## Authorship

Research leadership and contributor roles are documented in [CONTRIBUTORS.md](CONTRIBUTORS.md).
