from pydantic import BaseModel

from models.backstory import Backstory
from models.persona_fact import PersonaFact


class PersonaFactInput(BaseModel):
    backstory: Backstory
    existing_facts: list[PersonaFact]