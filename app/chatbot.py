"""Core chatbot logic: input validation, prompt building, reply interpretation."""

import json
from pathlib import Path

from app.prompts import OUT_OF_SCOPE_TOKEN, UNCLEAR_TOKEN, build_system_prompt

MAX_QUESTION_LENGTH = 500
DEFAULT_FAQ_PATH = Path(__file__).parent / "data" / "faq.json"

OUT_OF_SCOPE_MESSAGE = (
    "Sorry, I can only help with BilgiShop orders, shipping, returns, payments and accounts. "
    "/ Üzgünüm, bu konuda yardımcı olamıyorum."
)
UNCLEAR_MESSAGE = (
    "I could not understand your question. Could you please rephrase it? "
    "/ Sorunuzu anlayamadım, lütfen farklı bir şekilde yazar mısınız?"
)


class InvalidQuestionError(ValueError):
    """Raised when the user's question breaks the input rules (R1, R2)."""


def load_faq(path=DEFAULT_FAQ_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _is_token(reply, token):
    """True if the LLM reply is just the special token (ignoring case and punctuation)."""
    return reply.strip().strip(".!\"' ").upper() == token


class FAQChatbot:
    def __init__(self, llm_client, faq_entries=None, prompt_version="v1"):
        self.llm_client = llm_client
        self.faq_entries = faq_entries if faq_entries is not None else load_faq()
        self.system_prompt = build_system_prompt(self.faq_entries, prompt_version)

    def validate_question(self, question):
        """Check the input rules and return the cleaned question."""
        if not isinstance(question, str):
            raise InvalidQuestionError("Question must be a string.")
        cleaned = question.strip()
        if not cleaned:
            raise InvalidQuestionError("Question must not be empty.")
        if len(cleaned) > MAX_QUESTION_LENGTH:
            raise InvalidQuestionError(
                f"Question must be at most {MAX_QUESTION_LENGTH} characters."
            )
        return cleaned

    def ask(self, question):
        """Answer one question. Returns {"answer": str, "status": str}."""
        cleaned = self.validate_question(question)
        reply = self.llm_client.generate(self.system_prompt, cleaned)

        if _is_token(reply, OUT_OF_SCOPE_TOKEN):
            return {"answer": OUT_OF_SCOPE_MESSAGE, "status": "out_of_scope"}
        if _is_token(reply, UNCLEAR_TOKEN):
            return {"answer": UNCLEAR_MESSAGE, "status": "unclear"}
        return {"answer": reply, "status": "answered"}