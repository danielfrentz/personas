from pydantic import BaseModel, Field

from models.ai.output.story_ai import StoryAI
from models.backstory import Backstory


class CorrespondingStoryInput(BaseModel):
    original_story: StoryAI = Field(description="the original story, the new one is the same story told from a different lens.")
    corresponding_story_main_character: Backstory = Field(description="the main character of the new version of the story.")
    original_story_main_character: Backstory = Field(description="The main character of the original story.")