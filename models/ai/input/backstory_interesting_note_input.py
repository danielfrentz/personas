from pydantic import BaseModel


class BackstoryInterestingNoteInput(BaseModel):
    persona_description: str
    