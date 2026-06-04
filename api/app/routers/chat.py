from app.schemas.chat import MessageCreate, ChatResponse

from app.db.database import get_db

from app.db.models import Conversation
from app.db.models import Message

from app.llm import LLMService
from app.deps.conversation import get_conversation
from app.deps.llm import get_llm_service

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import json

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/{conversation_id}", response_model=ChatResponse)
async def chat(
    message: MessageCreate,
    conversation: Conversation = Depends(get_conversation),
    db: Session = Depends(get_db),
    llm: LLMService = Depends(get_llm_service)
):

    # 1. Save user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=message.content,
    )

    db.add(user_msg)
    db.commit()

    # 2. Load full history
    history = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.id)
        .all()
    )

    formatted = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    # 3. Call LLM
    reply = await llm.generate_chat(formatted)

    # 4. Save assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=reply,
    )

    db.add(assistant_msg)
    db.commit()


    # 5. Refresh Objects to guarantee IDs are populated
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    return ChatResponse(
        user_message=user_msg,
        assistant_message=assistant_msg
    )


@router.post("/{conversation_id}/stream")
async def chat_stream(
    payload: dict,
    conversation: Conversation = Depends(get_conversation),
    llm: LLMService = Depends(get_llm_service)
):
    async def event_stream():
        try:
            async for token in llm.stream_chat(payload["messages"]):
                yield f"data: {token}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: ERROR {str(e)}\n\n"
        
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )