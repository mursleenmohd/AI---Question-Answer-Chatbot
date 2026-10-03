from sqlalchemy import select
from backend.database import SessionLocal
from backend.models import Conversation, Message


def create_conversation():
    db = SessionLocal()
    try:
        conversation = Conversation()
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id
    finally:
        db.close()


def save_message(conversation_id: int, role: str, content: str,):
    db = SessionLocal()
    try:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()
    finally:
        db.close()


def get_messages(conversation_id: int,):
    db = SessionLocal()
    try:
        result = db.execute(
            select(Message).where(Message.conversation_id== conversation_id).order_by(Message.created_at)
        )
        return result.scalars().all()
    finally:
        db.close()