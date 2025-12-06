from typing import Optional

from pydantic import BaseModel


class RelationshipFeeling(BaseModel):
    id: Optional[int] = None
    persona_relationship_id: Optional[int]
    feeling_name: str
    reason: str