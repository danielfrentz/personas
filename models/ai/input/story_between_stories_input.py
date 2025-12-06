from pydantic import BaseModel

from models.persona import Persona
from models.story import Story


class StoryBetweenStoriesInput(BaseModel):
    main_character: Persona
    story_before: Story
    story_after: Story