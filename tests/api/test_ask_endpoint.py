"""API tests for POST /ask.

Techniques:
- Equivalence Partitioning (EP) on the request body: valid / empty / whitespace /
  missing field / wrong type
- Boundary Value Analysis (BVA) on question length: 499, 500 (valid) and 501, 502 (invalid)
"""

import pytest

from app.llm_client import LLMError


# ---- R4, R9: normal answer and response format ----

# Verifies: R4, R9
def test_valid_question_returns_200_and_answer(api):
    client, _ = api(reply="Refunds take 5 to 7 business days.")
    response = client.post("/ask", json={"question": "How long do refunds take?"})
    assert response.status_code == 200
    assert response.json() == {
        "answer": "Refunds take 5 to 7 business days.",
        "status": "answered",
    }


# Verifies: R9
def test_response_always_has_exactly_answer_and_status_fields(api):
    client, _ = api()
    body = client.post("/ask", json={"question": "Hello?"}).json()
    assert set(body.keys()) == {"answer", "status"}


# Verifies: R9
def test_response_is_json(api):
    client, _ = api()
    response = client.post("/ask", json={"question": "Hello?"})
    assert response.headers["content-type"].startswith("application/json")


# ---- R5, R6: special replies ----

# Verifies: R5
def test_out_of_scope_question_returns_200_with_out_of_scope_status(api):
    client, _ = api(reply="OUT_OF_SCOPE")
    response = client.post("/ask", json={"question": "Who won the match?"})
    assert response.status_code == 200
    assert response.json()["status"] == "out_of_scope"


# Verifies: R6
def test_unclear_question_returns_200_with_unclear_status(api):
    client, _ = api(reply="UNCLEAR")
    response = client.post("/ask", json={"question": "asdf ???"})
    assert response.status_code == 200
    assert response.json()["status"] == "unclear"


# ---- R1: invalid input (EP: invalid partitions) ----

# Verifies: R1
@pytest.mark.parametrize("question", ["", " ", "\t", "\n", " \t\n "])
def test_empty_or_whitespace_question_returns_422(api, question):
    client, llm = api()
    response = client.post("/ask", json={"question": question})
    assert response.status_code == 422
    assert llm.calls == []


# Verifies: R1
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"wrong_field": "How are you?"},
        {"question": None},
        {"question": 123},
        {"question": ["How are you?"]},
    ],
    ids=["empty-body", "wrong-field-name", "null", "number", "list"],
)
def test_missing_or_non_string_question_returns_422(api, payload):
    client, llm = api()
    response = client.post("/ask", json=payload)
    assert response.status_code == 422
    assert llm.calls == []


# Verifies: R1
def test_body_that_is_not_json_returns_422(api):
    client, _ = api()
    response = client.post(
        "/ask", content="this is not json", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


# ---- R2: length boundaries (BVA) ----

# Verifies: R2
@pytest.mark.parametrize("length", [499, 500])
def test_question_up_to_500_characters_returns_200(api, length):
    client, _ = api()
    response = client.post("/ask", json={"question": "a" * length})
    assert response.status_code == 200


# Verifies: R2
@pytest.mark.parametrize("length", [501, 502])
def test_question_over_500_characters_returns_422(api, length):
    client, llm = api()
    response = client.post("/ask", json={"question": "a" * length})
    assert response.status_code == 422
    assert llm.calls == []


# ---- R3, R7: trimming and Unicode ----

# Verifies: R3
def test_question_is_trimmed_before_reaching_the_llm(api):
    client, llm = api()
    client.post("/ask", json={"question": "  How can I track my order?  "})
    assert llm.calls[0][1] == "How can I track my order?"


# Verifies: R7
def test_turkish_characters_and_emoji_survive_the_round_trip(api):
    reply = "Kargo ücretsizdir 😊 İyi günler, şğüöç"
    client, llm = api(reply=reply)
    question = "Kargo ücreti ne kadar? 🚚"
    response = client.post("/ask", json={"question": question})
    assert response.status_code == 200
    assert response.json()["answer"] == reply
    assert llm.calls[0][1] == question


# ---- R8: LLM failure ----

# Verifies: R8
def test_llm_failure_returns_503(api):
    client, _ = api(error=LLMError("timeout"))
    response = client.post("/ask", json={"question": "How long does shipping take?"})
    assert response.status_code == 503


# Verifies: R8
def test_llm_failure_does_not_leak_internal_details(api):
    client, _ = api(error=LLMError("secret-key-abc123 rejected by upstream"))
    response = client.post("/ask", json={"question": "Hello?"})
    assert "abc123" not in response.text
    assert "upstream" not in response.text


# Verifies: R8
def test_missing_api_configuration_returns_503(monkeypatch):
    # No dependency override here: the real get_chatbot runs, but the
    # environment has no API key, so creating the client must fail cleanly.
    from fastapi.testclient import TestClient

    from app.main import app, get_chatbot

    get_chatbot.cache_clear()
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    client = TestClient(app)
    response = client.post("/ask", json={"question": "Hello?"})
    assert response.status_code == 503
    get_chatbot.cache_clear()


# ---- Extra: HTTP-level behaviour ----

def test_extra_fields_in_body_are_ignored(api):
    client, _ = api()
    response = client.post("/ask", json={"question": "Hello?", "extra": 1})
    assert response.status_code == 200


def test_get_on_ask_is_not_allowed(api):
    client, _ = api()
    assert client.get("/ask").status_code == 405


def test_unknown_path_returns_404(api):
    client, _ = api()
    assert client.get("/does-not-exist").status_code == 404