from typing import List

from pydantic import BaseModel, Field

from models.ai.output.universe_ai import UniverseDescriptionAI
from models.ai.output.universe_location_ai import UniverseLocationAI


class UniverseLocationInput(BaseModel):
    existing_locations: List[UniverseLocationAI] = Field(description="List of existing universe locations, new locations must be distinct from these.")
    universe_description: UniverseDescriptionAI = Field(description="Description of the universe in which the locations are located.")