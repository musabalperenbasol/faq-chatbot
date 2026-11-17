# BilgiShop FAQ Chatbot

A small FAQ chatbot for a fictional online store, built with FastAPI and the Google
Gemini API. The focus of the project is **testing**: a deterministic pytest suite
(unit + API level) that runs without internet or an API key, designed with
Equivalence Partitioning and Boundary Value Analysis.

Course project for CMPE 411 (AI-Driven Software Testing and Quality Assurance).

## Quick start (under 5 minutes)

Requirements: Python 3.11+ and git.

```bash
git clone https://github.com/YOUR_USERNAME/faq-chatbot.git
cd faq-chatbot
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest
```

All tests use a fake LLM, so **no API key and no internet connection are needed**.
Tests marked `live` (real LLM calls) are skipped by default.

Useful variants:

```bash
pytest -v                                        # one line per test
pytest --cov=app --cov-report=term-missing       # coverage
python tools/traceability.py                     # requirement -> test matrix
```

## Run the chatbot (optional, needs a Gemini API key)

```bash
cp .env.example .env             # then put your key into .env
uvicorn app.main:app --reload
```

Try it:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

Interactive API docs: http://127.0.0.1:8000/docs

## Project structure

| Path | Purpose |
|---|---|
| `app/main.py` | FastAPI endpoints (`POST /ask`, `GET /health`) and error mapping |
| `app/chatbot.py` | Core logic: input validation, prompt, reply interpretation |
| `app/llm_client.py` | The only module that calls the real LLM (Gemini) |
| `app/prompts.py` | Versioned system prompts |
| `app/data/faq.json` | FAQ content |
| `tests/unit/` | Unit tests (chatbot logic, validation, prompts) |
| `tests/api/` | API tests (HTTP status codes, JSON format, error handling) |
| `docs/requirements.md` | Requirements R1-R10 |
| `docs/traceability.md` | Generated requirement-to-test matrix |
| `docs/ai_evidence/` | Evidence for the AI element |

## Testing strategy

- **Two levels:** unit tests call the chatbot class directly; API tests call the HTTP
  endpoints through FastAPI's `TestClient`.
- **Fake LLM:** the real LLM is replaced by a `FakeLLM` so tests are fast, free and
  repeatable. Real-LLM behaviour is evaluated separately (live evaluation).
- **Test design techniques:** Equivalence Partitioning (question types, LLM reply
  types, invalid inputs) and Boundary Value Analysis (question length 0, 1, 2, 499,
  500, 501, 502).
- **Traceability:** every test is tagged with `# Verifies: R<n>`.