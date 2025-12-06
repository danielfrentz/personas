from pydantic import BaseModel


class DialogueRequirements(BaseModel):
    reasoning: str
    monologue: str