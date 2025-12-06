from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class PersonaAspectConversation(BaseModel):
    aspect_id: int
    conversation: Optional[Conversation]
    topic: str