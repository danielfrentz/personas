from pydantic import BaseModel


class SelfDescriptionConversationRequest(BaseModel):
    prompter_id: int
    persona_id: int
    topic: str
