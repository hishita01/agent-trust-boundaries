# Trust Boundaries and Oversight in Tool-Using Agents

**Research-engineering demonstration with an executable real-LLM evaluation adapter.**

## Research question
Do explicit trust-boundary instructions reduce unauthorized attempted actions in simulated tool workflows, compared to ordinary agent instructions, while preserving legitimate task completion?

## Reproducible artifacts
- 60 original synthetic cases across 12 task families, and 60 meaning-preserving stress variants.
- Development (9 families) and held-out (3 families) partitioning by task group.
- Paired baseline and guarded configurations; actions are `execute`, `escalate` or `reject`.
- Simulated read, update and messaging tools. They cannot access real external services.
- Executable evaluation, regression tests, JSON/CSV results, cluster bootstrap intervals, and charts.
- OpenAI-compatible inference adapter for real LLM comparisons, not executed in this release.

## Run it
See [PROJECT_START_HERE.md](PROJECT_START_HERE.md) for the exact one-command-at-a-time reproducibility workflow.

## Scientific caveats
- Toy outputs are intentionally deterministic and may exploit superficial keywords. They **do not** demonstrate safety, alignment or model robustness.
- The 60 examples include repeated templates; effective independent sample size is closer to the 12 task families, and even those share templates.
- Stress cases preserve intended outcomes but need independent human auditing to confirm every label.
- The baseline instruction is a simplified comparison condition, not a widely accepted state-of-the-art agent.
- Research claims require actual model inference, independent assessment and model-provenance reporting.

## Authorship
See [CONTRIBUTORS.md](CONTRIBUTORS.md).
