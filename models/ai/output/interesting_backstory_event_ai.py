from pydantic import BaseModel, Field


class InterestingBackstoryEventAI(BaseModel):
    name: str = Field(description="A 1-2 word name for the event.")
    description: str = Field(description="A description of the event.")
    reason_of_importance: str = Field(description="The reason of importance of the event for this particular person.")