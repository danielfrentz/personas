from typing import List

from pydantic import BaseModel

from models.ai.output.conversation_turn_ai import ConversationTurnAI


class BookTranslationAI(BaseModel):
    conversation_turns: List[ConversationTurnAI]