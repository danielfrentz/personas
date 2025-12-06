from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.life_event import LifeEvent
from models.story import Story
from models.universe_description import UniverseDescription


class StoryEnhancementInput(BaseModel):
    universe: UniverseDescription = Field(description="The universe in which the story is based.")
    main_character: Backstory = Field(description="the main character of the story")
    life_event: LifeEvent = Field(description="The life event upon which this story is based on.")
    story: Story = Field(description="The story which needs enhancing")