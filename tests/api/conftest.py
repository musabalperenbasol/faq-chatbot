"""Fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_chatbot


@pytest.fixture
def api(make_bot):
    """Return a function that builds (client, fake_llm) with a fake LLM behind the API.

    Usage in a test:  client, llm = api(reply="OUT_OF_SCOPE")
    """

    def _make(reply="Fake answer", error=None):
        bot, llm = make_bot(reply=reply, error=error)
        app.dependency_overrides[get_chatbot] = lambda: bot
        return TestClient(app), llm

    yield _make
    # Cleanup after every test so tests stay independent of each other.
    app.dependency_overrides.clear()