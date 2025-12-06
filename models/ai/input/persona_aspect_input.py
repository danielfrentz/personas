from pydantic import BaseModel

from models.backstory import Backstory


class PersonaAspectInput(BaseModel):
    backstory: Backstory
    aspect_name: str

