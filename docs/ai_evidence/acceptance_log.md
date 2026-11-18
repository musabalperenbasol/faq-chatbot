# Acceptance log for gen_v1

Source: raw/generated_v1.py (unedited), 34 test functions, 62 pytest cases.
Prediction made BEFORE running: exactly 1 failure (the RuntimeError test).
First run of the unedited file: 61 passed, 1 failed (raw/first_run_gen_v1.txt). Prediction matched.

## Decisions

| Decision | Test | Reason |
|---|---|---|
| Accepted as generated (30 functions) | all tests not listed below | Match the requirements, meaningful assertions |
| Modified | test_health_rejects_unsupported_http_method | Wrong `Verifies: R9` tag. No requirement covers HTTP 405, so it is relabelled as a robustness test. |
| Modified | test_ask_rejects_unsupported_http_method | Wrong `Verifies: R1` tag. Same reason. |
| Modified | test_ask_turkish_and_emoji_at_500_char_boundary_accepted | A leaked reasoning comment and a duplicate assignment were removed. Test logic unchanged. |
| Rejected | test_ask_returns_503_on_unexpected_exception_from_llm | Expects HTTP 503 when the LLM layer raises a plain RuntimeError. R8 only says "if the LLM fails" and is ambiguous. The real client wraps every LLM failure in LLMError, and mapping real bugs to 503 would hide defects (500 is the correct answer). The test failed because of a requirement ambiguity, not a code defect. |

## Weak test kept

test_llm_system_prompt_contains_all_faq_domains_and_restriction_instruction uses keyword
checks with any(), so it can pass even when FAQ content is missing. To be evaluated with
mutation testing.

## Findings

- The AI-generated test exposed an ambiguity in requirement R8 that our own tests had not questioned.
- Wrong traceability tags: 2 of 34 tests.
- Leaked reasoning text inside generated code: 1 of 34 tests.
- Interesting ideas we had not covered ourselves: trimming before the length check (raw 506
  chars, trimmed 500), Unicode characters at the 500/501 boundary, internal whitespace kept,
  system prompt identical across questions, injection text not leaking into the system prompt.

Edits to the accepted file are recorded in accepted_edits.diff.
