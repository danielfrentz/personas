from typing import Optional, List

from pydantic import BaseModel, Field

from models.backstory import Backstory


class LifeEventInput(BaseModel):
    backstory: Backstory = Field(description="The profile of the person")
    previous_life_events: List[str] = Field(description="The previous life_events")
    provided_title: Optional[str] = None
    provided_context: Optional[str] = None
    historical: bool

