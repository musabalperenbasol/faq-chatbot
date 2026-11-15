"""The only module that talks to the real LLM API (Google Gemini).

Keeping it in one place makes it easy to replace with a fake in tests.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from the project root, no matter where the program is started.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

REQUEST_TIMEOUT_SECONDS = 15


class LLMError(Exception):
    """Raised when the LLM call fails (network, quota, timeout, empty reply...)."""


class GeminiClient:
    def __init__(self, api_key=None, model=None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL")
        if not api_key or not self.model:
            raise LLMError("GEMINI_API_KEY and GEMINI_MODEL must be set in .env")
        self._client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=REQUEST_TIMEOUT_SECONDS * 1000),
        )

    def generate(self, system_prompt, user_message):
        """Send one question to the LLM and return its text answer."""
        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0,
                ),
            )
        except Exception as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc

        if not response.text:
            raise LLMError("LLM returned an empty response")
        return response.text.strip()