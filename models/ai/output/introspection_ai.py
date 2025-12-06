from pydantic import BaseModel, Field

from models.ai.output.conversation_ai import ConversationAI


class IntrospectionAI(BaseModel):
    personality_aspect_role: str
    introspection_topic: str
    internal_monologue: ConversationAI = Field(description="The internal monologue.")