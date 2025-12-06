from typing import Optional

from pydantic import BaseModel


class GroupReasoningStyle(BaseModel):
    id: Optional[int] = None
    persona_id: int
    assumed_role: str
    tone: str
    devils_advocate: bool
    sarcastic: bool
    reserved: bool
    witty: bool
    subtle: bool

