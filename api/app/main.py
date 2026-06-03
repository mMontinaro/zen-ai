from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.db.database import Base
from app.db.database import engine
from app.db.database import get_db

from app.db.models import Conversation
from app.db.models import Message

from app.schemas.chat import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)

import app.db.models

from app.llm import generate_chat

app = FastAPI(title="AI Workspace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "running"}


@app.post(
    "/conversations",
    response_model=ConversationResponse
)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    record = Conversation(
        title=conversation.title
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):
    return db.query(Conversation).all()


@app.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageResponse
)
def create_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    record = Message(
        conversation_id=conversation_id,
        role=message.role,
        content=message.content,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(Message.id)
        .all()
    )


@app.post("/chat/{conversation_id}")
async def chat(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 1. Save user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content,
    )

    db.add(user_msg)
    db.commit()

    # 2. Load full history
    history = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id)
        .all()
    )

    formatted = [
        {"role": m.role, "content": m.content}
        for m in history
    ]



    # 3. Call LLM
    reply = await generate_chat(formatted)

    # 4. Save assistant response
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=reply,
    )

    db.add(assistant_msg)
    db.commit()

    return {
        "user_message": message.content,
        "assistant_message": reply
    }