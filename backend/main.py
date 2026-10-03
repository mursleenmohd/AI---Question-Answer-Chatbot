from fastapi import FastAPI
from backend.routes.chat import router as chat_router
import logging
from backend.database import Base, engine
from backend import models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chatbot API",
    description="An API for an AI chatbot using FastAPI and OpenAI's GPT model.",
    version="1.0.0"
)

app.include_router(chat_router)

@app.get("/")
def home():

    logging.getLogger(__name__).info(
        "Health check requested"
    )

    return {
        "message": "AI Chatbot API is running"
    }
