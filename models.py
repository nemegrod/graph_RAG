from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = datetime.now()

class ChatHistory(BaseModel):
    messages: List[Message] = []
    
    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the chat history"""
        message = Message(role=role, content=content)
        self.messages.append(message)
    
    def get_messages_for_api(self) -> List[dict]:
        """Convert messages to format expected by OpenAI API"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def clear(self) -> None:
        """Clear all messages"""
        self.messages = []
    
    def get_last_n_messages(self, n: int) -> List[Message]:
        """Get the last n messages"""
        return self.messages[-n:] if len(self.messages) >= n else self.messages
