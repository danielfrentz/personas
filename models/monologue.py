from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class Monologue(BaseModel):
    id: Optional[int] = None
    theme: str
    speaker_id: Optional[int] = None
    prompter_id: Optional[int] = None
    prompt: str
    conversation: Conversation
    previous_monologue_int: Optional[int] = None
    deliverable: Optional[str]
    problem_type: Optional[str] = None
    trigger_word: Optional[str] = None


