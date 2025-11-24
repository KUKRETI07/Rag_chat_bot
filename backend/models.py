from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    chat_id: str

class Message(BaseModel):
    role: str
    content: str
    timestamp: str

class ChatHistory(BaseModel):
    id: str
    title: str
    timestamp: str
