from typing import Optional, List

from pydantic import BaseModel, Field

from models.conversation import Conversation
from models.relationship_feeling import RelationshipFeeling
from models.relationship_thought import RelationshipThought


class Relationship(BaseModel):
    id: Optional[int] = None
    source_id: int
    target_id: int
    thoughts: Optional[List[RelationshipThought]] = Field(default_factory=list)
    feelings: Optional[List[RelationshipFeeling]] = Field(default_factory=list)
    relationship_type: str
    relationship_subtype: str
    overall_description: str
    conversation: Optional[Conversation] = None
