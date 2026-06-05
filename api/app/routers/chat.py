from app.schemas.chat import MessageCreate, ChatResponse

from app.db.database import get_db

from app.db.models import Conversation
from app.db.models import Message

from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.deps.conversation_dep import get_conversation
from app.deps.llm_dep import get_llm_service
from app.deps.chat_dep import get_chat_service

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import json

from app.core.enums import Roles

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/{conversation_id}", response_model=ChatResponse)
async def chat(
    message: MessageCreate,
    conversation: Conversation = Depends(get_conversation),
    db: Session = Depends(get_db),
    llm: LLMService = Depends(get_llm_service),
    chat_service: ChatService = Depends(get_chat_service)
):

    # 1. Save user message
    user_msg = chat_service.save_message(db, Roles.USER, conversation.id, message.content)

    # 2. Load full history
    history = chat_service.load_full_history(db, conversation.id)

    formatted = chat_service.format_history(history)

    # 3. Call LLM
    reply = await llm.generate_chat(formatted)

    # 4. Save assistant response
    assistant_msg = chat_service.save_message(db, Roles.ASSISTANT, conversation.id, reply)
    
    return ChatResponse(
        user_message=user_msg,
        assistant_message=assistant_msg
    )


@router.post("/{conversation_id}/stream")
async def chat_stream(
    message: MessageCreate,
    conversation: Conversation = Depends(get_conversation),
    db: Session = Depends(get_db),
    llm: LLMService = Depends(get_llm_service),
    chat_service: ChatService = Depends(get_chat_service)

):
    # 1. Save user message
    chat_service.save_message(db, Roles.USER, conversation.id, message.content)

    # 2. Load full history
    history = chat_service.load_full_history(db, conversation.id)

    formatted = chat_service.format_history(history)

    async def event_stream():
        full_response=""
        print("ABOUT TO STREAM")
        try:
            async for token in llm.stream_chat(formatted):
                print("TOKEN:", repr(token))
                full_response+=token
                yield f"data: {token}\n\n"
            
            # Save assistant message
            print("FINAL:", repr(full_response))
            chat_service.save_message(db, Roles.ASSISTANT, conversation.id, full_response)
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: ERROR {str(e)}\n\n"
        
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )
