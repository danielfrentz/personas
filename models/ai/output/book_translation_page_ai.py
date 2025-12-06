from typing import List

from models.ai.output.conversation_turn_ai import ConversationTurnAI


class BookTranslationPageAI:
    passage: str
    conversation_turns: List[ConversationTurnAI]