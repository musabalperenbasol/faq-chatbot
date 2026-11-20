"""Unit tests for prompt versions (needed for prompt regression testing)."""

import pytest

from app.chatbot import FAQChatbot, load_faq
from app.prompts import OUT_OF_SCOPE_TOKEN, PROMPTS, UNCLEAR_TOKEN, build_system_prompt
from tests.conftest import FakeLLM


# Verifies: R10
@pytest.mark.parametrize("version", sorted(PROMPTS))
def test_every_prompt_version_keeps_faq_rule_and_markers(version):
    faq = load_faq()
    prompt = build_system_prompt(faq, version)
    assert "ONLY" in prompt
    assert OUT_OF_SCOPE_TOKEN in prompt
    assert UNCLEAR_TOKEN in prompt
    for entry in faq:
        assert entry["question"] in prompt
        assert entry["answer"] in prompt


# Verifies: R10
def test_prompt_versions_are_different():
    faq = load_faq()
    assert build_system_prompt(faq, "v1") != build_system_prompt(faq, "v2")


# Verifies: R10
def test_chatbot_uses_the_requested_prompt_version():
    # Kills __init__ mutant 12 (prompt_version argument dropped)
    llm = FakeLLM()
    bot = FAQChatbot(llm, prompt_version="v2")
    bot.ask("How long does shipping take?")
    assert llm.calls[0][0] == build_system_prompt(load_faq(), "v2")