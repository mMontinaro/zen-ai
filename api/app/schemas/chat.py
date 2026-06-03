from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str

    class Config:
        from_attributes = True