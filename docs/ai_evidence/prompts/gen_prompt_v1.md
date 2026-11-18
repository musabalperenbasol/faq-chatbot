You are a QA engineer. Write automated pytest tests for the REST API described below.
You have NOT seen the implementation. Base your tests only on the requirements.

## Requirements

# BilgiShop FAQ Chatbot: Requirements

The chatbot answers customer questions about BilgiShop (returns, shipping,
payments, accounts) using a fixed FAQ. It is exposed through a REST API.

## API

- `POST /ask` with JSON body `{"question": "<text>"}` returns `{"answer": "<text>", "status": "<status>"}`.
- `GET /health` returns `{"status": "ok"}`.
- `status` is one of `answered`, `out_of_scope`, `unclear`.

## Requirements

| ID | Requirement |
|---|---|
| R1 | An empty, whitespace-only, missing or non-string question is rejected with HTTP 422. The LLM is not called. |
| R2 | A question may have at most 500 characters (after trimming). A longer question is rejected with HTTP 422. |
| R3 | Leading and trailing whitespace is removed from the question before it is processed. |
| R4 | A question covered by the FAQ gets the LLM answer with `status` = `answered` (HTTP 200). |
| R5 | A valid question that the FAQ does not cover gets a fixed polite message with `status` = `out_of_scope` (HTTP 200). |
| R6 | A meaningless or unclear message (for example "asdf ???") gets a fixed request to rephrase with `status` = `unclear` (HTTP 200). The system does not crash. |
| R7 | Turkish characters (ç, ğ, ı, ö, ş, ü, İ) and emoji are processed correctly. |
| R8 | If the LLM fails (error, timeout, missing configuration), the API returns HTTP 503 with a generic message. Internal error details are not exposed. |
| R9 | `/ask` always returns JSON with exactly the fields `answer` and `status`. `/health` returns `{"status": "ok"}`. |
| R10 | The prompt sent to the LLM contains every FAQ entry and an instruction to answer only from the FAQ. |

## Test harness (already exists, do not redefine it)

- Application: `from app.main import app`
- Fixture `api` is available in every test. Call `client, llm = api(reply="...", error=None)`.
  It returns a FastAPI TestClient whose LLM is replaced by a fake.
  - `reply`: the text the fake LLM returns. To simulate the LLM saying a question is not
    covered by the FAQ it returns exactly `"OUT_OF_SCOPE"`; for a meaningless message it
    returns exactly `"UNCLEAR"`; any other text is a normal answer.
  - `error`: an exception instance the fake LLM raises, for example `LLMError("timeout")`
    (`from app.llm_client import LLMError`).
  - `llm.calls`: list of `(system_prompt, user_message)` tuples, one per LLM call.
- For `/health` no fixture is needed: `TestClient(app).get("/health")`.

## Instructions

1. Write pytest tests in ONE Python file. Test the API only (HTTP status codes, JSON body, LLM calls).
2. Apply Equivalence Partitioning and Boundary Value Analysis explicitly. Add a short comment
   naming the partition or boundary each test covers. Use `pytest.mark.parametrize` where suitable.
3. Put a comment line `# Verifies: R<n>` (for example `# Verifies: R2` or `# Verifies: R4, R9`)
   directly above every test function.
4. Include negative tests and tests you think are likely to expose bugs.
5. Tests must be independent, deterministic, and must not use the network, sleep, or a real LLM.
6. Write between 25 and 35 test functions with descriptive names.
7. Output only one Python code block, no explanations.
