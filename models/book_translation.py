from typing import List

from pydantic import BaseModel

from models.conversation_turn import ConversationTurn


class BookTranslation(BaseModel):
    passage: str
    conversation_turns: List[ConversationTurn]