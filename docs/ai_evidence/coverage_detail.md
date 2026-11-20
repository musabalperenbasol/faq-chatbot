# Coverage gaps of the AI suite (verified with term-missing)

The AI suite (61 tests) covers 86% of the app, our suite 92%. Extra uncovered lines:

| Line | File | Code | Reason |
|---|---|---|---|
| 44 | app/chatbot.py | raise InvalidQuestionError("Question must be a string.") | FastAPI rejects non-string input before the chatbot is called; only a unit test reaches it. |
| 27 | app/main.py | return FAQChatbot(GeminiClient()) in get_chatbot() | The AI simulated "missing configuration" with a fake that raises LLMError, so the real get_chatbot never ran. |
| 25-28 | app/llm_client.py | GeminiClient.__init__ key check | Same reason. |

Finding: the AI test named test_ask_returns_503_on_missing_configuration_without_exposing_details
does not execute any configuration check. Its name promises more than it tests. This became
visible only through coverage.

Lines 29 and 36-50 of llm_client.py (client creation and the real API call) are not covered
by any suite on purpose: the real LLM is replaced by a fake in all default tests.
