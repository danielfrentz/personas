from typing import Optional

from pydantic import BaseModel


class ConversationTurn(BaseModel):
    id: Optional[int] = None
    speaker: str
    action: Optional[str] = None
    turn_intent: Optional[str] = None
    private_thought: Optional[str] = None
    tone: str
    directed_at: list[str]
    feeling: str
    placement: Optional[int] = None
    text: str

