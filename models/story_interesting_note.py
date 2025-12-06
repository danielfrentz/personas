from typing import Optional

from pydantic import BaseModel


class StoryInterestingNote(BaseModel):
    id: Optional[int] = None
    name: str
    details: str
    story_id: int
