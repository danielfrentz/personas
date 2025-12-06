from pydantic import BaseModel

from models.backstory import Backstory


class InitialRelationshipInput(BaseModel):
    source_persona: Backstory
    target_persona: Backstory