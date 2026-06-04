from app.schemas.chat import MessageCreate, MessageResponse

from app.db.database import get_db

from app.db.models import Conversation, Message

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/conversations",
    tags=["messages"]
)

@router.post(
    "/{conversation_id}/messages",
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


@router.get(
    "/{conversation_id}/messages",
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