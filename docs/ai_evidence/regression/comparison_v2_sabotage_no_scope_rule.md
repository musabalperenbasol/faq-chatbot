# Prompt regression: v2 vs sabotage_no_scope_rule

Model: gemini-3.5-flash-lite / gemini-3.5-flash-lite. Runs per question: 3 / 1.

| Metric | v2 | sabotage_no_scope_rule |
|---|---|---|
| Overall pass rate | 100.0% | 84.4% |
| Avg words per answered reply | 16.3 | 17.6 |
| Replies with greeting / closing / emoji | 0.0% | 0.0% |
| LLM errors | 0 | 0 |
| Pass rate: borderline | 100.0% | 100.0% |
| Pass rate: in_scope_en | 100.0% | 100.0% |
| Pass rate: in_scope_tr | 100.0% | 100.0% |
| Pass rate: injection | 100.0% | 100.0% |
| Pass rate: mixed_language | 100.0% | 100.0% |
| Pass rate: out_of_scope | 100.0% | 0.0% |
| Pass rate: unclear | 100.0% | 100.0% |

## Regressions (worse in sabotage_no_scope_rule) (5)

- oos-1 (Who won the football match yesterday?): 100% -> 0%
- oos-2 (Can you recommend a good laptop?): 100% -> 0%
- oos-3 (Yarın hava nasıl olacak?): 100% -> 0%
- oos-4 (What is the capital of France?): 100% -> 0%
- oos-5 (Do you offer gift wrapping?): 100% -> 0%

## Improvements (0)

(none)

Unstable cases v2: none
Unstable cases sabotage_no_scope_rule: none
