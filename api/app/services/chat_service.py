from sqlalchemy.orm import Session

from app.db.models import Message

class ChatService:

    def save_message(
            self,
            db: Session, 
            role: str, 
            conversation_id: int, 
            message_content: str
    ) -> Message:
    
        # Creates msg, saves it to db, and refreshes Objects to guarantee populated ID
        msg = Message(
            conversation_id = conversation_id,
            role=role,
            content=message_content
        )

        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    def load_full_history(
            self,
            db: Session, 
            conversation_id: int
    ):
        
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.id)
            .all()
        )

    def format_history(
            self,
            history
    ):
        return [
            {
                "role": m.role,
                "content": m.content,
            } for m in history
        ]