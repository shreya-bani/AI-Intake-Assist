from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime


class Message(BaseModel):
    """A single message in the conversation."""
    role: Literal["system", "user", "assistant"]
    content: str


class ConversationHistory(BaseModel):
    """Complete conversation history for a session."""
    messages: List[Message] = Field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append(Message(role=role, content=content))

    def get_messages_dict(self) -> List[dict]:
        """Get messages as list of dicts for LLM API."""
        return [msg.model_dump() for msg in self.messages]

    def get_user_messages_only(self) -> List[Message]:
        """Get only user messages."""
        return [msg for msg in self.messages if msg.role == "user"]


class MessageRequest(BaseModel):
    """Request model for sending a message."""
    message: str = Field(..., min_length=1, description="User message content")


class MessageResponse(BaseModel):
    """Response model after processing a message."""
    assistant_message: str = Field(..., description="AI assistant's response")
    updated_fields: dict = Field(default_factory=dict, description="Newly updated form fields")
    is_complete: bool = Field(default=False, description="Whether all required fields are filled")
