from typing import Optional

from pydantic import BaseModel


class Memory(BaseModel):
    id: Optional[int] = None
    memory_text: str
    core_memory: bool
    feelings_stirred: str
    memory_reflex: str
    story_title: Optional[str] = None
    story_id: Optional[int] = None
    memory_reflex_followup: str