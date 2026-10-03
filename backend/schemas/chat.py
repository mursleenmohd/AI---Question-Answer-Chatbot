from typing import Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)


class AIResponse(BaseModel):
    answer: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    difficulty: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]


class ChatResponse(BaseModel):
    answer: str
    topic: str
    difficulty: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]