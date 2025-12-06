from pydantic import BaseModel


class AccessoryConversationRequest(BaseModel):
    prompter_id: int
    wearer_id: int