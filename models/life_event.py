from typing import Optional

from pydantic import BaseModel, Field

from models.story import Story


class LifeEvent(BaseModel):
    id: Optional[int] = None
    detail_learned: str = Field(description="What was learned about the persona.")
    title: str = Field(description="The title of the event.")
    description: str = Field(description="An indepth description of what happened and why this was important.")
    date: str = Field(description="The date of the event, if unknow then a description relative to others.")
    persona_id: int = Field(description="The persona id of the event.")
    story: Optional[Story] = Field(description="The story associated with this event.", default=None)
