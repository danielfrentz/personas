from pydantic import BaseModel, Field

from models.ai.output.conversation_ai import ConversationAI


class MonologueAI(BaseModel):
    conversation: ConversationAI
    deliverable: str = Field(description="The deliverable of the monologue.")

