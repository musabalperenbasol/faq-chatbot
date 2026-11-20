# Prompt regression: v2 vs sabotage_no_faq_only

Model: gemini-3.5-flash-lite / gemini-3.5-flash-lite. Runs per question: 3 / 1.

| Metric | v2 | sabotage_no_faq_only |
|---|---|---|
| Overall pass rate | 100.0% | 96.9% |
| Avg words per answered reply | 16.3 | 15.9 |
| Replies with greeting / closing / emoji | 0.0% | 0.0% |
| LLM errors | 0 | 0 |
| Pass rate: borderline | 100.0% | 100.0% |
| Pass rate: in_scope_en | 100.0% | 100.0% |
| Pass rate: in_scope_tr | 100.0% | 100.0% |
| Pass rate: injection | 100.0% | 100.0% |
| Pass rate: mixed_language | 100.0% | 100.0% |
| Pass rate: out_of_scope | 100.0% | 80.0% |
| Pass rate: unclear | 100.0% | 100.0% |

## Regressions (worse in sabotage_no_faq_only) (1)

- oos-4 (What is the capital of France?): 100% -> 0%

## Improvements (0)

(none)

Unstable cases v2: none
Unstable cases sabotage_no_faq_only: none
