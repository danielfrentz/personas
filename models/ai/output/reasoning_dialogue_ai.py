from typing import List

from pydantic import BaseModel

from models.conversation_turn import ConversationTurn


class ReasoningDialogueAI(BaseModel):
    conversation: List[ConversationTurn]