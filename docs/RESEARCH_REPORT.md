# Research report: Agent trust boundaries and safe tool-action attempts

**Status:** executable evaluation framework and toy demonstration, **not an LLM research result**.

## Abstract
We implement a paired synthetic evaluation framework to measure whether explicit trust-boundary instructions change a tool-using language model's tendency to execute authorized actions, follow adversarial text from retrieved documents, or escalate uncertain cases. A simulated sandbox records attempted tool name and destination; no real external actions occur. The repository includes a deterministic toy mode to validate plumbing and an API adapter for model-based experiments. No empirical model claims are made until actual LLM runs and independent review are completed.

## Hypotheses
H1: Explicit trust-boundary instructions decrease attempted unauthorized redirections on attack-bearing contexts. H2: Oversight may raise incorrect refusals on otherwise authorized tasks. H3: Policies that memorize attack wording will generalize poorly to held-out domains and paraphrases.

## Dataset and evaluation
60 synthetic scenarios in 12 task families. Nine families are development cases; three are held out, with task-family partitioning to reduce leakage. Each task has clean and injected contexts, plus insufficient-authorization and explicitly unauthorized requests. The paired attacks preserve authorized user intent and vary only external context. Ground-truth labels come from the dataset construction rubric and **have not been independently adjudicated**.

## Measurements
Exact action accuracy, attempted unsafe tool rate (simulation proxy), redirection rate on attacked context, authorized clean-case task success, escalation recall, wall-clock latency and returned token counts. Descriptive Wilson intervals are displayed but do not adjust for template clustering.

## Results
**Toy deterministic smoke test:** see `results/toy_demo_metrics.json`. These do not measure LLM behavior.

**Live model evaluation:** NOT RUN — API access required. Insert actual model name, evaluation date, data hash, per-split results and confidence intervals only after executing a live experiment.

## Key limitations
1. Synthetic, formulaic cases with correlated templates and small held-out partition.
2. Ground truth not independently annotated; labels may bake in designer assumptions.
3. Single-step proposed decisions and simulated tools, not autonomous long-horizon agents.
4. Prompt variants differ in several instructions, not a clean ablation of individual causes.
5. No claims about deployment safety or reliability are warranted from simulation.

## Authorship and ethics
Report scaffold were produced with generative AI assistance and require human review. Record collaborators' real contributions. The simulated actions make no modifications to external systems and contain no sensitive information.
