from typing import List, Optional

from pydantic import BaseModel, Field

from converter.story_disagreement import StoryDisagreement
from models.introspection import Introspection
from models.memory import Memory
from models.story_interesting_note import StoryInterestingNote


class Story(BaseModel):
    id: Optional[int] = None
    title: str
    characters: Optional[List[str]] = Field(default_factory=list)
    life_event_id: Optional[int] = None
    lead_up: str
    story: Optional[str] = None
    outcome: str
    interesting_notes: Optional[List[StoryInterestingNote]] = Field(default_factory=list)
    disagreements: Optional[List[StoryDisagreement]] = Field(default_factory=list)
    memories: Optional[List[Memory]] = Field(default_factory=list)
    introspections: Optional[List[Introspection]] = Field(default_factory=list)

