from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base
from app.db.database import engine

from app.routers.conversations import router as conversations_router
from app.routers.messages import router as messages_router
from app.routers.chat import router as chat_router

app = FastAPI(title="AI Workspace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(chat_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "running"}