"""Unit tests for prompt building (R10)."""

import pytest

from app.chatbot import load_faq
from app.prompts import OUT_OF_SCOPE_TOKEN, UNCLEAR_TOKEN, build_system_prompt


# Verifies: R10
def test_prompt_contains_every_faq_question_and_answer():
    faq = load_faq()
    prompt = build_system_prompt(faq)
    for entry in faq:
        assert entry["question"] in prompt
        assert entry["answer"] in prompt


# Verifies: R10
def test_prompt_contains_only_faq_rule_and_special_tokens():
    prompt = build_system_prompt(load_faq())
    assert "ONLY" in prompt
    assert OUT_OF_SCOPE_TOKEN in prompt
    assert UNCLEAR_TOKEN in prompt


# Verifies: R10
def test_prompt_uses_custom_faq_entries():
    custom = [{"id": 1, "question": "Do you sell cats?", "answer": "No, only books."}]
    prompt = build_system_prompt(custom)
    assert "Do you sell cats?" in prompt
    assert "What is your return policy?" not in prompt


# Verifies: R10
def test_unknown_prompt_version_raises_error():
    with pytest.raises(KeyError):
        build_system_prompt(load_faq(), version="does-not-exist")