from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class Introspection(BaseModel):
    id: Optional[int] = None
    personality_aspect_role: str
    introspection_topic: str
    monologue: Optional[Conversation] = None
    story_id: int
    aspect_id: Optional[int] = None