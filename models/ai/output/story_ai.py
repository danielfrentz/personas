from typing import List

from pydantic import BaseModel, Field


class StoryAI(BaseModel):
    story_title: str = Field(description="The title of the story")
    characters: List[str] = Field(description="A list of character names that appear in the story.")
    lead_up: str = Field(description="The lead up of the story. should be descriptive")
    story: str = Field(description="A summary of the story, not too long but enough detail so the user knows what happened.")
    outcome: str = Field(description="The outcome of the story.")
    attributes_shown: List[str] = Field(description="A list of attributes that were shown to the user.")
    things_person_learned: List[str] = Field(description="A list of things that the person learned.")
