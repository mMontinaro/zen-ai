from app.schemas.chat import ConversationCreate, ConversationResponse

from app.db.database import get_db

from app.db.models import Conversation

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)


@router.post(
    "",
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

@router.get(
    "",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):
    return db.query(Conversation).all()