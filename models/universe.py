from typing import Optional, List

from pydantic import BaseModel, Field

from models.persona import Persona
from models.universe_description import UniverseDescription
from models.universe_location import UniverseLocation
from models.universe_metadata import UniverseMetadata


class Universe(BaseModel):
    id: Optional[int] = None
    name: str
    description: UniverseDescription = None
    metadata: Optional[List[UniverseMetadata]] = Field(default_factory=list)
    personas: Optional[List[Persona]] = Field(default_factory=list)
    locations: Optional[List[UniverseLocation]] = Field(default_factory=list)


