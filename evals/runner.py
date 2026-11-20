"""Live evaluation of the FAQ chatbot with the REAL LLM.

Not part of the default test run. Usage (from the project root):
    python -m evals.runner --prompt v1 --runs 3
Results go to docs/ai_evidence/regression/results_<prompt>.json
"""

import argparse
import json
import os
import re
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

from app.chatbot import FAQChatbot
from app.llm_client import GeminiClient, LLMError

HERE = Path(__file__).resolve().parent
EVAL_SET_PATH = HERE / "eval_set.json"
RESULTS_DIR = HERE.parent / "docs" / "ai_evidence" / "regression"

# "Filler" = greetings, closing offers and emoji. Prompt v2 tries to remove them.
FILLER = re.compile(
    r"^\s*(hello|hi|hey|merhaba|selam)\b|let us know|any more help|başka bir sorunuz"
    r"|[\U0001F300-\U0001FAFF\u2600-\u27BF]",
    re.IGNORECASE,
)


def load_cases():
    return json.loads(EVAL_SET_PATH.read_text(encoding="utf-8"))


def check_case(case, result):
    """Return a list of problems. An empty list means the case passed."""
    problems = []
    expected = case["expected_status"]
    if result["status"] not in expected:
        problems.append(f"status {result['status']!r}, expected one of {expected}")
    answer = result["answer"].lower()
    keywords = case.get("must_contain_any", [])
    if result["status"] == "answered" and keywords:
        if not any(k.lower() in answer for k in keywords):
            problems.append(f"answer contains none of {keywords}")
    for forbidden in case.get("must_not_contain", []):
        if forbidden.lower() in answer:
            problems.append(f"answer contains forbidden text {forbidden!r}")
    return problems


def ask_with_retry(bot, question, delay, retries=3):
    """Ask the bot; wait between calls (free-tier rate limit) and retry on LLM errors."""
    for attempt in range(retries + 1):
        try:
            result = bot.ask(question)
            time.sleep(delay)
            return result
        except LLMError as exc:
            if attempt == retries:
                return {"answer": f"LLM_ERROR: {exc}", "status": "llm_error"}
            time.sleep(20 * (attempt + 1))


def evaluate(prompt_version, runs=3, delay=4.0, system_prompt=None):
    bot = FAQChatbot(GeminiClient(), prompt_version=prompt_version)
    if system_prompt is not None:
        bot.system_prompt = system_prompt  # experiment: override the prompt
    records = []
    for case in load_cases():
        for run in range(1, runs + 1):
            result = ask_with_retry(bot, case["question"], delay)
            problems = check_case(case, result)
            records.append(
                {
                    "id": case["id"],
                    "category": case["category"],
                    "question": case["question"],
                    "run": run,
                    "status": result["status"],
                    "answer": result["answer"],
                    "passed": not problems,
                    "problems": problems,
                    "words": len(result["answer"].split()),
                    "filler": bool(FILLER.search(result["answer"])),
                }
            )
    return records


def summarize(records):
    by_category = defaultdict(list)
    by_case = defaultdict(list)
    for r in records:
        by_category[r["category"]].append(r["passed"])
        by_case[r["id"]].append(r["passed"])
    answered = [r for r in records if r["status"] == "answered"]
    return {
        "pass_rate": sum(r["passed"] for r in records) / len(records),
        "by_category": {c: sum(v) / len(v) for c, v in by_category.items()},
        "llm_errors": sum(r["status"] == "llm_error" for r in records),
        "avg_words_answered": (sum(r["words"] for r in answered) / len(answered)) if answered else 0,
        "filler_rate_answered": (sum(r["filler"] for r in answered) / len(answered)) if answered else 0,
        "unstable_cases": sorted(c for c, v in by_case.items() if 0 < sum(v) < len(v)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="v1")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--delay", type=float, default=4.0)
    parser.add_argument("--sabotage", default=None, help="name from evals/sabotaged_prompts.py")
    args = parser.parse_args()

    label = args.prompt
    system_prompt = None
    if args.sabotage:
        from evals.sabotaged_prompts import build_sabotaged
        system_prompt = build_sabotaged(args.sabotage)
        label = f"sabotage_{args.sabotage}"
    records = evaluate(args.prompt, args.runs, args.delay, system_prompt)
    summary = summarize(records)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / f"results_{label}.json"
    payload = {
        "prompt": label,
        "model": os.getenv("GEMINI_MODEL"),
        "date": date.today().isoformat(),
        "runs": args.runs,
        "summary": summary,
        "records": records,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    for r in records:
        if not r["passed"]:
            print(f"FAIL {r['id']} (run {r['run']}): {r['problems']}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("Saved:", out)


if __name__ == "__main__":
    main()