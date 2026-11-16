"""Unit tests for how the chatbot interprets the LLM reply.

Technique: Equivalence Partitioning on the LLM reply:
normal answer / OUT_OF_SCOPE marker / UNCLEAR marker / LLM failure.
"""

import pytest

from app.chatbot import OUT_OF_SCOPE_MESSAGE, UNCLEAR_MESSAGE
from app.llm_client import LLMError


# Verifies: R4
def test_normal_llm_reply_is_returned_as_answered(make_bot):
    bot, _ = make_bot(reply="Refunds take 5 to 7 business days.")
    result = bot.ask("How long do refunds take?")
    assert result == {"answer": "Refunds take 5 to 7 business days.", "status": "answered"}


# Verifies: R5
def test_out_of_scope_marker_gives_fixed_message(make_bot):
    bot, _ = make_bot(reply="OUT_OF_SCOPE")
    result = bot.ask("Who won the football match?")
    assert result == {"answer": OUT_OF_SCOPE_MESSAGE, "status": "out_of_scope"}


# Verifies: R5
@pytest.mark.parametrize("reply", ["out_of_scope", "OUT_OF_SCOPE.", "  Out_Of_Scope\n"])
def test_out_of_scope_marker_variants_are_recognised(make_bot, reply):
    bot, _ = make_bot(reply=reply)
    assert bot.ask("Who won the football match?")["status"] == "out_of_scope"


# Verifies: R6
def test_unclear_marker_asks_user_to_rephrase(make_bot):
    bot, _ = make_bot(reply="UNCLEAR")
    result = bot.ask("asdf ???")
    assert result == {"answer": UNCLEAR_MESSAGE, "status": "unclear"}


# Verifies: R4, R5, R6
def test_marker_word_inside_a_normal_sentence_is_not_a_marker(make_bot):
    # Only a reply that IS the marker counts; a sentence that merely contains it does not.
    bot, _ = make_bot(reply="Your order status is UNCLEAR until it ships.")
    assert bot.ask("Where is my order?")["status"] == "answered"


# Verifies: R8
def test_llm_failure_is_not_hidden_by_the_chatbot(make_bot):
    bot, _ = make_bot(error=LLMError("timeout"))
    with pytest.raises(LLMError):
        bot.ask("How long does shipping take?")