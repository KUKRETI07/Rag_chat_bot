import json
import os
import uuid
from typing import List, Dict

HISTORY_FILE = "chat_history.json"

def load_history() -> Dict[str, List[Dict]]:
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_history(history: Dict[str, List[Dict]]):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_all_chats():
    history = load_history()
    # Return list of chats with ID and first message/title
    chats = []
    for chat_id, messages in history.items():
        title = "New Chat"
        if messages:
            # Use first user message as title, truncated
            for msg in messages:
                if msg["role"] == "user":
                    title = msg["content"][:30] + "..."
                    break
        chats.append({"id": chat_id, "title": title, "timestamp": messages[-1]["timestamp"] if messages else ""})
    # Sort by timestamp desc (if we had timestamps properly, for now just reverse)
    return list(reversed(chats))

def get_chat_messages(chat_id: str):
    history = load_history()
    return history.get(chat_id, [])

def create_new_chat():
    chat_id = str(uuid.uuid4())
    history = load_history()
    history[chat_id] = []
    save_history(history)
    return chat_id

def add_message(chat_id: str, role: str, content: str):
    history = load_history()
    if chat_id not in history:
        history[chat_id] = []
    
    import datetime
    timestamp = datetime.datetime.now().isoformat()
    
    history[chat_id].append({
        "role": role,
        "content": content,
        "timestamp": timestamp
    })
    save_history(history)
