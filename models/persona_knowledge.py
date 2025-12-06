from typing import Optional

from pydantic import BaseModel


class PersonaKnowledge(BaseModel):
    id: Optional[int] = None
    persona_id: int
    knowledge_name: str
    knowledge_description: str
