"""Tests added after the first mutation analysis (stage 9a).

Each test names the surviving mutants it is meant to kill. They live in a
separate file so the baseline suite can still be measured without them.
"""

import pytest

from app.chatbot import InvalidQuestionError, load_faq
from app.prompts import build_system_prompt, format_faq

CUSTOM_FAQ = [
    {"id": 1, "question": "Do you sell cats?", "answer": "No, only books."},
    {"id": 2, "question": "Do you sell dogs?", "answer": "No, only pens."},
]


# Verifies: R10
def test_format_faq_exact_layout():
    # Kills format_faq mutants 9 and 11 (entry separator and line joiner)
    expected = (
        "Q: Do you sell cats?\n"
        "A: No, only books.\n"
        "\n"
        "Q: Do you sell dogs?\n"
        "A: No, only pens."
    )
    assert format_faq(CUSTOM_FAQ) == expected


# Verifies: R10
def test_chatbot_sends_its_system_prompt_to_the_llm(make_bot):
    # Kills __init__ mutant 8 (system_prompt = None) and ask mutant 4 (generate(None, ...))
    bot, llm = make_bot()
    bot.ask("How long does shipping take?")
    assert llm.calls[0][0] == build_system_prompt(load_faq())


# Verifies: R10
def test_chatbot_builds_prompt_from_custom_faq_entries(make_bot):
    # Kills __init__ mutant 5 (custom FAQ entries ignored)
    bot, llm = make_bot(faq_entries=CUSTOM_FAQ)
    bot.ask("Do you sell cats?")
    sent_prompt = llm.calls[0][0]
    assert "Do you sell cats?" in sent_prompt
    assert "What is your return policy?" not in sent_prompt


# Verifies: R4, R5, R6
@pytest.mark.parametrize("reply", ["XOUT_OF_SCOPEX", "XXOUT_OF_SCOPEXX", "XUNCLEARX"])
def test_marker_with_extra_letters_is_not_a_marker(make_bot, reply):
    # Kills _is_token mutant 3 (letter X added to the characters that get stripped).
    # Only whitespace and punctuation around the marker may be ignored.
    bot, _ = make_bot(reply=reply)
    assert bot.ask("Where is my order?")["status"] == "answered"


# Verifies: R1, R2
@pytest.mark.parametrize(
    "bad_question", [None, "", "a" * 501], ids=["non-string", "empty", "too-long"]
)
def test_validation_error_has_a_real_message(make_bot, bad_question):
    # Kills validate_question mutants 2, 8, 13 (message replaced by None).
    # The API returns this text to the user, so it must not be empty or "None".
    bot, _ = make_bot()
    with pytest.raises(InvalidQuestionError) as exc_info:
        bot.ask(bad_question)
    message = str(exc_info.value).strip()
    assert message != ""
    assert message != "None"