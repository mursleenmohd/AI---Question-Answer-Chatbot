from fastapi import APIRouter, HTTPException
import logging
from fastapi.responses import StreamingResponse
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.database_service import create_conversation
from backend.services.llm_service import get_llm_response, stream_llm_response

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/conversations")
def create_new_conversation():
    conversation_id = create_conversation()
    return {
        "conversation_id": conversation_id
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:

        logger.info("Chat request received")

        result = get_llm_response(
            message=request.message,
            history=request.history,
        )

        logger.info("LLM response generated successfully")

        return ChatResponse(
            answer=result.answer,
            topic=result.topic,
            difficulty=result.difficulty,
        )

    except Exception:
        logger.exception("Error while processing chat request")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate a response from the AI service.",
        )

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    try:
        logger.info("Streaming request received")
        return StreamingResponse(
            stream_llm_response(
                message=request.message,
                history=request.history,
            ),
            media_type="text/plain",
        )
    except Exception:
        logger.exception("Streaming failed")
        raise HTTPException(
            status_code=502,
            detail="Unable to stream AI response.",
        )