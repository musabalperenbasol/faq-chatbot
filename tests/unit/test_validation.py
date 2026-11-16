"""Unit tests for input validation.

Test design techniques used:
- Equivalence Partitioning (EP): empty / whitespace-only / non-string / valid inputs
- Boundary Value Analysis (BVA): question length around the 500-character limit

The limit 500 is written as a literal number on purpose: if someone changes the
constant in the code by mistake, these tests must fail.
"""

import pytest

from app.chatbot import InvalidQuestionError


# ---- R1: empty and whitespace-only input (EP: invalid partition) ----

# Verifies: R1
@pytest.mark.parametrize("question", ["", " ", "     ", "\t", "\n", " \t\n "])
def test_empty_or_whitespace_question_is_rejected(make_bot, question):
    bot, llm = make_bot()
    with pytest.raises(InvalidQuestionError):
        bot.ask(question)
    assert llm.calls == []  # the LLM must not be called for invalid input


# Verifies: R1
@pytest.mark.parametrize("question", [None, 123, ["How are you?"]])
def test_non_string_question_is_rejected(make_bot, question):
    bot, llm = make_bot()
    with pytest.raises(InvalidQuestionError):
        bot.ask(question)
    assert llm.calls == []


# ---- R2: length limit (BVA) ----
# Valid range is 1..500 characters. Invalid: 0 (tested above) and 501+.

# Verifies: R2
@pytest.mark.parametrize("length", [1, 2, 499, 500])
def test_length_inside_limit_is_accepted(make_bot, length):
    bot, llm = make_bot()
    result = bot.ask("a" * length)
    assert result["status"] == "answered"
    assert len(llm.calls) == 1


# Verifies: R2
@pytest.mark.parametrize("length", [501, 502, 1000])
def test_length_above_limit_is_rejected(make_bot, length):
    bot, llm = make_bot()
    with pytest.raises(InvalidQuestionError):
        bot.ask("a" * length)
    assert llm.calls == []


# ---- R3: trimming ----

# Verifies: R3
def test_surrounding_whitespace_is_removed_before_sending(make_bot):
    bot, llm = make_bot()
    bot.ask("   How long does shipping take?  \n")
    assert llm.calls[0][1] == "How long does shipping take?"


# Verifies: R2, R3
def test_padding_spaces_do_not_count_toward_length_limit(make_bot):
    bot, _ = make_bot()
    result = bot.ask("  " + "a" * 500 + "  ")  # 504 raw characters, 500 after trimming
    assert result["status"] == "answered"


# ---- R7: Turkish characters and emoji ----

# Verifies: R7
def test_turkish_characters_and_emoji_reach_the_llm_unchanged(make_bot):
    bot, llm = make_bot()
    question = "Şifremi nasıl sıfırlarım? 😊 ğüşiöç İI"
    result = bot.ask(question)
    assert llm.calls[0][1] == question
    assert result["status"] == "answered"