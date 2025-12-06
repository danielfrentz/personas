from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class SelfDescriptionConversation(BaseModel):
    id: Optional[int] = None
    conversation: Optional[Conversation] = None
    persona_id: int
    prompter_id: int
    topic: str