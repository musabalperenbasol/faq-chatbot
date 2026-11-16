"""API tests for GET /health."""

from fastapi.testclient import TestClient

from app.main import app


# Verifies: R9
def test_health_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Verifies: R9
def test_health_does_not_need_the_llm():
    # /health must work even if the LLM is not configured: it never calls the chatbot.
    client = TestClient(app)
    assert client.get("/health").status_code == 200