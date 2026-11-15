"""FastAPI application: HTTP layer of the FAQ chatbot."""

from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.chatbot import FAQChatbot, InvalidQuestionError
from app.llm_client import GeminiClient, LLMError

app = FastAPI(title="BilgiShop FAQ Chatbot")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    status: str


@lru_cache
def get_chatbot():
    """Create the real chatbot once and reuse it. Tests replace this function."""
    return FAQChatbot(GeminiClient())


@app.exception_handler(InvalidQuestionError)
async def invalid_question_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(LLMError)
async def llm_error_handler(request, exc):
    # Do not leak internal error details to the client.
    return JSONResponse(
        status_code=503,
        content={"detail": "The assistant is temporarily unavailable. Please try again later."},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest, chatbot: FAQChatbot = Depends(get_chatbot)):
    return chatbot.ask(body.question)