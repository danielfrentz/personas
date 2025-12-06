from typing import List, Optional

from pydantic import BaseModel

from models.conversation_turn import ConversationTurn


class Conversation(BaseModel):
    id: Optional[int] = None
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    conversation_turns: List[ConversationTurn]
