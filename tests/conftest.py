"""Shared test helpers (fixtures) used by unit and API tests."""

import pytest

from app.chatbot import FAQChatbot


class FakeLLM:
    """A fake LLM client: returns a fixed reply or raises a fixed error.

    It records every call so tests can check what the chatbot sent.
    """

    def __init__(self, reply="Fake answer", error=None):
        self.reply = reply
        self.error = error
        self.calls = []  # list of (system_prompt, user_message)

    def generate(self, system_prompt, user_message):
        self.calls.append((system_prompt, user_message))
        if self.error is not None:
            raise self.error
        return self.reply


@pytest.fixture
def make_bot():
    """Return a function that builds (chatbot, fake_llm) for a given fake reply."""

    def _make(reply="Fake answer", error=None, faq_entries=None):
        llm = FakeLLM(reply=reply, error=error)
        return FAQChatbot(llm, faq_entries=faq_entries), llm

    return _make