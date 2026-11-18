# Mutation analysis of our own suite (tool: mutmut 3.8.1)

Scope: app/chatbot.py, app/prompts.py, app/main.py, app/__init__.py.
Excluded on purpose: app/llm_client.py (the real Gemini call is never executed by the
fake-LLM tests; its mutants would measure "mocked away", not "weak tests").
AI-generated tests were excluded from these runs (--ignore in pyproject.toml).

## Result

| Run | Tests | Killed | Survived | Score |
|---|---|---|---|---|
| Baseline (our 61 tests) | 61 | 71 | 19 | 78.9% |
| After gap-filling tests (our 61 + 9 new cases) | 70 | 80 | 10 | 88.9% |

Prediction made before the second run: 80/90 (9 mutants killed). Observed: 80/90.
Coverage was already 100% for chatbot.py, main.py and prompts.py at baseline, so the 19
survivors show what line coverage cannot see.

## Baseline survivors, classified

### Group 1: real gaps (9 mutants), killed by new tests in tests/unit/test_mutation_gaps.py

| Mutant | Change | Why it survived | Killed by |
|---|---|---|---|
| __init__ _8 | system_prompt = None | No test checked which system prompt the chatbot sends to the LLM | test_chatbot_sends_its_system_prompt_to_the_llm |
| ask _4 | generate(None, cleaned) | Same | same test |
| __init__ _5 | custom faq_entries ignored | No test passed a custom FAQ to FAQChatbot | test_chatbot_builds_prompt_from_custom_faq_entries |
| format_faq _9 | entry separator "" -> "XXXX" | Tests only checked that FAQ text appears in the prompt, not its layout | test_format_faq_exact_layout |
| format_faq _11 | line joiner changed | Same | same test |
| _is_token _3 | letter X added to stripped characters | Only punctuation stripping was tested, not "other characters must stay" | test_marker_with_extra_letters_is_not_a_marker |
| validate_question _2, _8, _13 | error message replaced by None | Tests checked exception type and status code, not the message the user sees | test_validation_error_has_a_real_message |

Most important finding: R10 says the LLM prompt must contain the FAQ. We tested the prompt
builder, but never that the chatbot actually passes the prompt to the LLM. Tests were
green and coverage was 100%, yet this gap existed in our own hand-designed suite.

### Group 2: equivalent or environment-dependent (4 mutants), no test added

| Mutant | Change | Reason |
|---|---|---|
| load_faq _6 | "utf-8" -> "UTF-8" | Python treats both names as the same encoding. True equivalent mutant. |
| load_faq _2, _4 | encoding removed | Equivalent on this machine: macOS defaults to UTF-8 and faq.json is plain ASCII. Would be a real bug on Windows with Turkish characters in the FAQ. |
| __init__ _12 | prompt_version argument dropped | Equivalent while only prompt version v1 exists. To be killed in stage 9c when v2 is added. |

### Group 3: unspecified behaviour (6 mutants), deliberately not killed

validate_question _3, _4, _5, _9, _10, _11 change the wording of the error messages
(extra characters, lower case, upper case). The requirements only demand HTTP 422, not
exact text. Asserting exact wording would make tests brittle (a wording fix would break
them). We only assert that a message exists and is not "None" (Group 1).

Rule applied: a mutant is killed only if the behaviour it breaks is specified.

## Remaining survivors after gap filling (10)

load_faq _2, _4, _6 (Group 2), __init__ _12 (Group 2), validate_question _3, _4, _5, _9,
_10, _11 (Group 3). All are explained above. No unexplained survivor remains.

## Evidence files

- baseline_ours_run.txt, baseline_ours_survivors.txt, baseline_ours_survivors_detail.txt
- after_gaps_run.txt, after_gaps_survivors.txt
