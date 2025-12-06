from typing import List, Optional

from pydantic import BaseModel

from models.relationship import Relationship
from models.story import Story


class RelationshipInput(BaseModel):
    main_character: str
    existing_relationships: List[Relationship]
    story: Optional[Story] = None