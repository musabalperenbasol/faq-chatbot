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