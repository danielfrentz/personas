from pydantic import BaseModel, Field


class InterestingBackstoryNoteAI(BaseModel):
    name: str = Field(description="A 1-2 word name for the note.")
    description: str = Field(description="A description of the note.")