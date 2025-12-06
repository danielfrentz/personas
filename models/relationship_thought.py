from typing import Optional

from pydantic import BaseModel


class RelationshipThought(BaseModel):
    id: Optional[int] = None
    thought: str
