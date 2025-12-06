from pydantic import BaseModel


class PersonaAspectConversationRequest(BaseModel):
    topic: str
    aspect_name: str
    persona_id: int
