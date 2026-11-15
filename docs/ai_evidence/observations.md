# AI Observations Log

Model used: gemini-3.5-flash-lite (checked 15 Nov 2026)

| Date | Observation | Relevance |
|---|---|---|
| 15 Nov | `gemini-2.5-flash-lite` appears in the model list but returns 404 for new users. | Listed != usable. |
| 15 Nov | `gemini-3.1-flash-lite` answered "Ping" when asked for exactly "pong". | LLMs do not always follow exact-output instructions. |
| 15 Nov | Prompt v1 manual check: 4/4 questions behaved as expected (answered, answered in Turkish, out_of_scope, unclear). | Baseline for regression tests. |
| 15 Nov | Bot adds extra friendly sentences to FAQ answers. | Live tests must check key facts, not exact text. |
| 15 Nov | API check: the bot starts answers with "Hello!" and ends with "Let us know if you need any more help!", even for a one-line FAQ answer. | Confirms exact-text assertions are fragile in live tests. |