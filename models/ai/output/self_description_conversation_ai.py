from pydantic import BaseModel

from models.ai.output.conversation_ai import ConversationAI


class SelfDescriptionConversationAI(BaseModel):
    conversation: ConversationAI
