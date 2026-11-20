"""Live evaluation test: calls the REAL LLM. Skipped by default.

Run with:  python -m pytest -m live
Choose the prompt version with:  PROMPT_VERSION=v2 python -m pytest -m live
"""

import os

import pytest

from evals.runner import evaluate, summarize

pytestmark = pytest.mark.live

PASS_RATE_THRESHOLD = 0.85


def test_eval_set_pass_rate_is_above_threshold():
    version = os.getenv("PROMPT_VERSION", "v1")
    records = evaluate(version, runs=1, delay=4.0)
    failures = [f"{r['id']}: {r['problems']}" for r in records if not r["passed"]]
    rate = summarize(records)["pass_rate"]
    assert rate >= PASS_RATE_THRESHOLD, f"{rate:.0%} for prompt {version}; failures: {failures}"