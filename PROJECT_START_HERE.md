# START HERE — reproducible complete offline project

Python 3.10+ required. Run these commands from this project directory:

```bash
python -m unittest discover -s tests -v
python -m src.dataset
python -m src.robustness
python -m src.run --mode toy --data data/scenarios_v2.jsonl --out results/original
python -m src.run --mode toy --data data/stress_scenarios.jsonl --out results/stress
python -m src.analysis results/original/toy_demo_predictions.csv results/stress/toy_demo_predictions.csv --out results/analysis
```

View `results/analysis/unsafe_attempt_rates.png`, `results/analysis/analysis.csv`, and `docs/FINAL_RESEARCH_REPORT.md`.

**Critical:** The runs above test deterministic toy policies. They are not LLM experiments. Real inference requires a model endpoint/API key or running the script against an accessible locally hosted OpenAI-compatible endpoint. Never commit credentials.

```bash
export LLM_BASE_URL='http://localhost:8000/v1'
export LLM_MODEL='YOUR_LOCAL_MODEL_NAME'
export LLM_API_KEY='local-token'
python -m src.run --mode llm --data data/scenarios_v2.jsonl --repeats 3 --out results/live-original
python -m src.run --mode llm --data data/stress_scenarios.jsonl --repeats 3 --out results/live-stress
```

The OpenAI-compatible adapter does not launch or download a local model server for you. When configuring it, use only an endpoint you have permission to access.
