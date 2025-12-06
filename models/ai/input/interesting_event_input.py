from pydantic import BaseModel


class InterestingEventInput(BaseModel):
    persona_description: str