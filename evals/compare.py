"""Compare two evaluation result files. Usage: python -m evals.compare v1 v2"""

import json
import sys
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "docs" / "ai_evidence" / "regression"


def load(version):
    return json.loads((DIR / f"results_{version}.json").read_text(encoding="utf-8"))


def case_rates(payload):
    rates, questions = defaultdict(list), {}
    for r in payload["records"]:
        rates[r["id"]].append(r["passed"])
        questions[r["id"]] = r["question"]
    return {k: sum(v) / len(v) for k, v in rates.items()}, questions


def main(old="v1", new="v2"):
    a, b = load(old), load(new)
    sa, sb = a["summary"], b["summary"]
    rates_a, questions = case_rates(a)
    rates_b, _ = case_rates(b)

    lines = [
        f"# Prompt regression: {old} vs {new}",
        "",
        f"Model: {a['model']} / {b['model']}. Runs per question: {a['runs']} / {b['runs']}.",
        "",
        "| Metric | " + old + " | " + new + " |",
        "|---|---|---|",
        f"| Overall pass rate | {sa['pass_rate']:.1%} | {sb['pass_rate']:.1%} |",
        f"| Avg words per answered reply | {sa['avg_words_answered']:.1f} | {sb['avg_words_answered']:.1f} |",
        f"| Replies with greeting / closing / emoji | {sa['filler_rate_answered']:.1%} | {sb['filler_rate_answered']:.1%} |",
        f"| LLM errors | {sa['llm_errors']} | {sb['llm_errors']} |",
    ]
    for cat in sorted(sa["by_category"]):
        lines.append(f"| Pass rate: {cat} | {sa['by_category'][cat]:.1%} | {sb['by_category'].get(cat, 0):.1%} |")

    regressions = [c for c in rates_a if rates_b.get(c, 0) < rates_a[c]]
    improvements = [c for c in rates_a if rates_b.get(c, 0) > rates_a[c]]
    for title, ids in (("Regressions (worse in " + new + ")", regressions), ("Improvements", improvements)):
        lines += ["", f"## {title} ({len(ids)})", ""]
        lines += [f"- {c} ({questions[c]}): {rates_a[c]:.0%} -> {rates_b[c]:.0%}" for c in ids] or ["(none)"]

    lines += ["", f"Unstable cases {old}: {sa['unstable_cases'] or 'none'}", f"Unstable cases {new}: {sb['unstable_cases'] or 'none'}"]
    text = "\n".join(lines) + "\n"
    (DIR / f"comparison_{old}_{new}.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(*sys.argv[1:3])