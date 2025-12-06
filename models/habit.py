from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class Habit(BaseModel):
    id: Optional[int] = None
    backstory_id: Optional[int] = None
    name: str
    frequency: str
    description: str
    good_habit: bool
    internal_monologue: Optional[Conversation] = None