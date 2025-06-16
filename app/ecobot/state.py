#state.py
from typing import List, Dict, Any, TypedDict

class Message(TypedDict):
    role: str
    content: str

class BotState(TypedDict):
    messages: List[Message]
    last_accion: str
