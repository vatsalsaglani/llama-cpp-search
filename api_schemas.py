from pydantic import BaseModel, Field
from typing import List, Literal, Dict


class Message(BaseModel):
    role: Literal["user", "system", "assistant"]
    content: str


class Conversation(BaseModel):
    messages: List[Message]


class ChatPayload(BaseModel):
    messages: List[Dict]
    max_tokens: int = 256
    resp_type: Literal["complete", "stream"]
