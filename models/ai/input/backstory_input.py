from pydantic import BaseModel

from models.universe_description import UniverseDescription


class BackstoryInput(BaseModel):
    name: str
    initial_character_description: str
    universe: UniverseDescription
    historical: bool