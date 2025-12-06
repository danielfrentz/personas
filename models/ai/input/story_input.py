from typing import List

from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.life_event import LifeEvent
from models.universe_description import UniverseDescription


class StoryInput(BaseModel):
    universe_description: UniverseDescription = Field(description="The universe in which the story is based.")
    main_character: Backstory
    life_event: LifeEvent = Field(description="The life event upon which this story is based on.")
    existing_characters: List[Backstory] = Field(description="The existing characters of the universe")

