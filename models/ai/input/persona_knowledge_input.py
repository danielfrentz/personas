from pydantic import BaseModel

from models.backstory import Backstory


class PersonaKnowledgeInput(BaseModel):
    backstory: Backstory
