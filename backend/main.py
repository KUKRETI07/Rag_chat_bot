from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Import local modules
from rag import run_llm, initialize_rag
from history import get_all_chats, get_chat_messages, create_new_chat, add_message
from models import ChatRequest, ChatResponse, ChatHistory, Message

app = FastAPI(title="RAG Chatbot API")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG on startup
@app.on_event("startup")
async def startup_event():
    initialize_rag()

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        chat_id = request.chat_id
        if not chat_id:
            chat_id = create_new_chat()
        
        # Save user message
        add_message(chat_id, "user", request.message)
        
        # Get AI response
        ai_response = run_llm(request.message)
        
        # Save AI response
        add_message(chat_id, "assistant", ai_response)
        
        return ChatResponse(response=ai_response, chat_id=chat_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=List[ChatHistory])
async def get_history():
    return get_all_chats()

@app.get("/history/{chat_id}", response_model=List[Message])
async def get_chat_history(chat_id: str):
    messages = get_chat_messages(chat_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return messages

@app.post("/new", response_model=ChatResponse)
async def start_new_chat():
    chat_id = create_new_chat()
    return ChatResponse(response="New chat started", chat_id=chat_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
