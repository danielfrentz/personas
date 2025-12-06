from pydantic import BaseModel

from models.ai.output.conversation_turn_ai import ConversationTurnAI


class ConversationAI(BaseModel):
    conversation_turn_count: int
    conversation_turns: list[ConversationTurnAI]