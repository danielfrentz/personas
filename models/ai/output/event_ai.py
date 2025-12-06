from typing import List

from pydantic import BaseModel, Field


class EventAI(BaseModel):
    title: str = Field(description="The title of the story")
    character_names: List[str] = Field(description="A list of character names that appear in the story.")
    lead_up: str = Field(description="The lead up of the story. should be descriptive")
    neutral_retelling: str = Field(description="A summary of the story, not too long but enough detail so the user knows what happened.")
    outcome: str = Field(description="The outcome of the story.")