# Improving research validity

1. Independently review scenario labels, record disagreements and reasons, and remove or revise ambiguous tasks before running final evaluation.
2. Freeze held-out cases before prompt iteration. Do not optimize prompts against held-out results.
3. Evaluate at least two different models, if accessible. Pin model IDs, provider, dates, temperature, retries and prompt versions.
4. Use 3+ repeated trials per model and variant; report each trial and aggregate variation. Do not claim independent samples for templates.
5. Add task-group bootstrap confidence intervals and compare policies with paired tests at the group level.
6. Increase external validity with independently written attacks, paraphrases, unseen domains, longer context and multi-step tool flows. Avoid including real private data.
7. Manually inspect true and false positives; characterize redirection, over-refusal, schema errors, and misses.
8. Conduct small ablations: instruction hierarchy alone, escalation instruction alone, and both. Pre-register hypotheses where possible.
9. Do not infer real-world harm prevention from simulated tool decisions.

