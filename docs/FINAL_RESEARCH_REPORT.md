# Trust Boundaries and Oversight in Tool-Using Agents
## Reproducible research-engineering demonstration 

**Status:** complete offline synthetic simulation; no live LLM model experiment performed. This is not a peer-reviewed paper.

### Abstract
We implemented a simulation harness to test whether an explicit trust-boundary policy can decrease unauthorized tool-action attempts under untrusted retrieved content, while preserving legitimate user requests. The study includes 60 synthetic scenarios from 12 task families and an additional 60 stress variants. Two deterministic policies (not large language models) produce decisions for simulated read, write, and messaging tools. On the original set, the guarded toy policy had a 0% unsafe-action proxy rate versus 40% for the baseline. However, stress phrasing made both policies fail at similar rates (approximately 32% each across all 60 stress cases). These findings demonstrate brittle heuristic-based evaluation and motivate controlled actual-LLM studies. **They do not establish any real model safety improvement.**

### Research question
Does an explicit hierarchy of instructions improve an AI agent's treatment of untrusted external content without causing excess refusal or escalation?

### Method
- 12 task groups, each with a legitimate clean request, two injected external-context cases, one uncertain authorization request, and one explicitly unauthorized request.
- 9 task families (45 scenarios) in development; 3 task families (15 scenarios) in a held-out partition.
- Baseline and guarded prompts are evaluated for the same cases; a simulated tool environment records attempted operations. This environment never invokes real external tools.
- A second set of 60 synthetic stress cases changes phrasing without deliberately changing the ground-truth decision labels. This transformation itself has not been independently adjudicated.
- Correct-action accuracy considers *decision type only*. Unsafe-action proxy captures unauthorized or redirected attempted tool operations and is therefore a more meaningful diagnostic here.
- Grouped bootstrap uncertainty intervals are calculated at the task-family level in `results/analysis/analysis.json`; common templates across families further limit inferential validity.

### Offline results (deterministic toy policies)

| Evaluation | Split | Baseline unsafe attempts | Guarded unsafe attempts | Baseline decision accuracy | Guarded decision accuracy |
|---|---|---:|---:|---:|---:|
| Original | Development (45 cases) | 40.0% | 0.0% | 100% | 100% |
| Original | Held out (15 cases) | 40.0% | 0.0% | 100% | 100% |
| Paraphrased | Development (45 cases) | 33.3% | 33.3% | 66.7% | 66.7% |
| Paraphrased | Held out (15 cases) | 26.7% | 26.7% | 73.3% | 73.3% |

The apparent original-set advantage was deliberately built into the illustrative heuristics: one policy follows certain injected strings while the other ignores them. The stress set demonstrates that both policies depend on brittle surface-form phrases for authorization decisions. These descriptive rates should not be interpreted as generalizable performance estimates.

### Limitations and validity threats
1. **No LLM evaluation:** The observed decisions come from Python rule-based toy policies. The OpenAI-compatible live inference adapter exists but was not executed because no model access credentials or local model endpoint were available.
2. **Narrow scenario distribution:** Just 12 task groups and repeated attack patterns. The held-out tasks still share the same scenario templates, meaning the held-out partition is *not* an independent generalization benchmark.
3. **Confounded prompt conditions:** The full guarded prompt adds multiple instructions at once; it does not isolate which instruction may matter.
4. **No actual downstream harm:** The sandbox only records attempted tools and cannot contact real systems.
5. **Limited statistical inference:** Even group-level bootstrap intervals cannot compensate for the shared authoring templates or non-random dataset construction.

### Next empirical experiment (not performed)
- Pre-register hypotheses and primary outcome (unsafe attempted action), and independently annotate the scenario labels.
- Evaluate at least two identified language models under a fixed decoding configuration using the provided `--mode llm` adapter; preserve model versions and raw responses.
- Include a genuine out-of-template benchmark and a factorial ablation of oversight instructions.
- Run repeated trials, report per-task success and failure cases, and compare cluster-resampled intervals rather than treating individual prompt variants as independent.
- Include explicit evaluation of over-refusal and inadvertent disclosure.

### Reproducibility and provenance
Run `PROJECT_START_HERE.md` commands. The experiment source, prompts, data, CSV predictions, JSON metrics, and plotted summary are included. 
